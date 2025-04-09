const draggableItems = document.querySelectorAll('.draggable-item');
const droppableAreaRows = document.getElementById('droppable-area-rows');
const droppableAreaCols = document.getElementById('droppable-area-cols');
const initialList = document.getElementById('initial-list');
const tableContainer = document.getElementById('table-container');
const filterContainer = document.getElementById('filter-container');

let rowColumns = [];
let colColumns = [];
let tableData = [];
let filteredTableData = [];

draggableItems.forEach(item => {
    item.addEventListener('dragstart', handleDragStart);
});

droppableAreaRows.addEventListener('dragover', handleDragOver);
droppableAreaRows.addEventListener('drop', event => handleDrop(event, 'row'));

droppableAreaCols.addEventListener('dragover', handleDragOver);
droppableAreaCols.addEventListener('drop', event => handleDrop(event, 'col'));

initialList.addEventListener('dragover', handleDragOver);
initialList.addEventListener('drop', event => handleDrop(event, 'initial'));

function handleDragStart(event) {
    event.dataTransfer.setData('text/plain', event.target.dataset.column);
    event.dataTransfer.setData('source-id', event.target.id); // Ajoute l'ID pour identifier l'origine
}

function handleDragOver(event) {
    event.preventDefault();
}

function handleDrop(event, type) {
    event.preventDefault();
    const column = event.dataTransfer.getData('text/plain');
    const sourceId = event.dataTransfer.getData('source-id');
    const draggedElement = document.querySelector(`[data-column="${column}"][id="${sourceId}"]`) || document.querySelector(`[data-column="${column}"]`);

    if (!draggedElement) return;

    // Supprimer l'élément de sa zone d'origine
    if (draggedElement.parentElement) {
        draggedElement.parentElement.removeChild(draggedElement);
    }

    // Retirer des tableaux rowColumns ou colColumns si nécessaire
    if (rowColumns.includes(column)) {
        rowColumns.splice(rowColumns.indexOf(column), 1);
    } else if (colColumns.includes(column)) {
        colColumns.splice(colColumns.indexOf(column), 1);
    }

    // Ajouter à la nouvelle zone
    if (type === 'row' && !rowColumns.includes(column)) {
        rowColumns.push(column);
        addColumnToArea(column, droppableAreaRows, rowColumns, type);
    } else if (type === 'col' && !colColumns.includes(column)) {
        colColumns.push(column);
        addColumnToArea(column, droppableAreaCols, colColumns, type);
    } else if (type === 'initial') {
        addColumnToArea(column, initialList, null, type);
    }

    // Cacher les placeholders si des éléments sont présents
    togglePlaceholders();

    sendColumnsToServer();
}

function addColumnToArea(column, area, columnList, type) {
    const newItem = document.createElement('div');
    newItem.classList.add('draggable-item');
    newItem.textContent = column;
    newItem.setAttribute('draggable', 'true');
    newItem.setAttribute('data-column', column);
    newItem.id = `drag-${column}-${Date.now()}`; // ID unique pour éviter les conflits
    newItem.addEventListener('dragstart', handleDragStart);

    // Supprimer l'élément au clic (sauf dans initial-list)
    if (type !== 'initial') {
        newItem.addEventListener('click', function () {
            area.removeChild(newItem);
            if (columnList) {
                columnList.splice(columnList.indexOf(column), 1);
            }
            togglePlaceholders();
            sendColumnsToServer();
        });
    }

    area.appendChild(newItem);
}

function togglePlaceholders() {
    const rowPlaceholder = droppableAreaRows.querySelector('#placeholder-rows');
    const colPlaceholder = droppableAreaCols.querySelector('#placeholder-cols');
    rowPlaceholder.style.display = droppableAreaRows.children.length > 1 ? 'none' : 'block';
    colPlaceholder.style.display = droppableAreaCols.children.length > 1 ? 'none' : 'block';
}

function sendColumnsToServer() {
    fetch('/process_columns', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            row_columns: rowColumns,
            col_columns: colColumns,
            value_column: 'Valeur'
        })
    })
    .then(response => response.json())
    .then(data => {
        tableData = data.data.map(row => {
            const rowData = {};
            data.columns.forEach((col, index) => {
                rowData[col.join(' ')] = row[index];
            });
            return rowData;
        });

        tableData.columns = data.columns;
        filteredTableData = tableData;
        generateTable(data);
        generateFilters();
    })
    .catch(error => console.error('Erreur:', error));
}

// Le reste des fonctions (generateTable, generateFilters, applyFilters, etc.) reste inchangé
// Assurez-vous d'inclure ces fonctions dans votre fichier JS si elles ne sont pas déjà présentes

function generateTable(data) {
    tableContainer.innerHTML = '';

    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    const columns = data.columns;
    const levels = columns.length > 0 ? columns[0].length : 0;

    for (let level = 0; level < levels; level++) {
        const headerRow = document.createElement('tr');
        let previousValue = null;
        let colspan = 0;

        columns.forEach((col, index) => {
            const currentValue = col[level];

            if (currentValue === previousValue) {
                colspan += 1;
            } else {
                if (colspan > 0) {
                    headerRow.lastChild.setAttribute('colspan', colspan);
                }
                const th = document.createElement('th');
                th.textContent = currentValue || '';
                headerRow.appendChild(th);
                previousValue = currentValue;
                colspan = 1;
            }

            if (index === columns.length - 1 && colspan > 1) {
                headerRow.lastChild.setAttribute('colspan', colspan);
            }
        });
        thead.appendChild(headerRow);
    }

    data.data.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach((col, index) => {
            const colKey = col.join(' ');
            const td = document.createElement('td');
            td.textContent = row[index] || ' ';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    tableContainer.appendChild(table);
}

// Ajoutez ici les autres fonctions (generateFilters, applyFilters, etc.) si elles ne sont pas déjà incluses


// Déclaration de lastValidValues en dehors de la fonction pour conserver les valeurs
const lastValidValues = {}; // Stockage des dernières valeurs valides par colonne

function generateFilters() {
    filterContainer.innerHTML = '';

    const allRows = [...rowColumns];
    const allColumns = [...colColumns];

    console.log("Columns for filters:", allRows);
    console.log('Columns for no filter:', allColumns);

    allRows.forEach(col => {
        // Vérifier si la colonne est dans colColumns, auquel cas on ne génère pas de filtre
        if (colColumns.includes(col)) {
            return; // Ignore les colonnes dans colColumns
        }

        const colKey = Array.isArray(col) ? col.join(' ') : col;
        let uniqueValues = [...new Set(tableData.map(row => row[colKey]))];

        // Filtrer les valeurs undefined
        uniqueValues = uniqueValues.filter(val => val !== undefined);

        // Si aucune valeur unique n'est trouvée, utiliser les dernières valeurs valides
        if (uniqueValues.length === 0) {
            uniqueValues = lastValidValues[colKey] || ["Valeur manquante"];
        } else {
            // Mettre à jour les dernières valeurs valides pour cette colonne
            lastValidValues[colKey] = uniqueValues;
        }

        console.log(`Unique values for ${colKey}:`, uniqueValues);
        console.log('Valeur stockées', lastValidValues);

        // Créez un conteneur de filtre dépliable
        const filterGroup = document.createElement('div');
        filterGroup.classList.add('filter-group');

        // Titre du filtre avec fonctionnalité de dépliage/repliage
        const filterTitle = document.createElement('div');
        filterTitle.classList.add('filter-title');
        filterTitle.innerHTML = `<span class="icon-orange">&#43;</span> Filtrer sur ${col}`;
        filterTitle.style.cursor = 'pointer';

        // Conteneur des cases à cocher (initialement masqué)
        const checkboxContainer = document.createElement('div');
        checkboxContainer.classList.add('checkbox-container');
        checkboxContainer.style.display = 'none';  // Commence replié

        // Ajouter l'événement de clic pour déplier/replier
        filterTitle.addEventListener('click', () => {
            checkboxContainer.style.display = 
                checkboxContainer.style.display === 'none' ? 'block' : 'none';
        });

        // Créez des cases à cocher pour chaque valeur unique, en gérant les valeurs undefined
        uniqueValues.forEach(value => {
            const checkboxWrapper = document.createElement('div');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = value;
            checkbox.setAttribute('data-column', colKey);

            const checkboxLabel = document.createElement('label');
            checkboxLabel.textContent = value;

            checkbox.addEventListener('change', applyFilters);

            checkboxWrapper.appendChild(checkbox);
            checkboxWrapper.appendChild(checkboxLabel);
            checkboxContainer.appendChild(checkboxWrapper);
        });

        // Ajoutez le titre et les options au groupe de filtres
        filterGroup.appendChild(filterTitle);
        filterGroup.appendChild(checkboxContainer);
        filterContainer.appendChild(filterGroup);
    });
}




function doesRowMatchFilters(row, filters) {
    // Pour chaque clé de filtre, vérifiez si la ligne contient une valeur correspondante
    return Object.keys(filters).every(column => {
        const filterValues = filters[column];
        
        // Vérifiez toutes les valeurs de la ligne qui pourraient correspondre à la colonne filtrée
        return Object.values(row).some(rowValue => filterValues.includes(rowValue));
    });
}
function applyFilters() {
    filteredTableData = [...tableData];  // Copie de données pour appliquer les filtres
    console.log("Applying filters...");
  
    const checkedCheckboxes = filterContainer.querySelectorAll('input[type="checkbox"]:checked');
    const filters = {};
  
    // Collecte des filtres sélectionnés
    checkedCheckboxes.forEach(checkbox => {
        const column = checkbox.getAttribute('data-column');
        const value = checkbox.value;

        // Utilisez la clé normalisée pour les filtres
        if (!filters[column]) {
            filters[column] = [];
        }
        filters[column].push(value);
    });

    // Application des filtres en utilisant `doesRowMatchFilters`
    filteredTableData = filteredTableData.filter(row => doesRowMatchFilters(row, filters));

    console.log('tableau obtenir', filteredTableData);

    // Regénérer le tableau avec les données filtrées
    generateTable({
        columns: tableData.columns,
        data: filteredTableData.map(row => {
            return tableData.columns.map(col => {
                const key = Array.isArray(col) ? col.join(' ') : col;  // Utilisez la clé normalisée
                return row[key];
            });
        })
    });
}






function mergeTableCells() {
    const table = document.querySelector('#table-container table');
    const rows = table.rows;
    const rowCount = rows.length;

    for (let col = 0; col < rows[0].cells.length; col++) {
        let startRow = 0;
        let value = rows[0].cells[col].innerText;
        for (let row = 1; row <= rowCount; row++) {
            if (row < rowCount && rows[row].cells[col].innerText === value) {
                continue;
            } else {
                if (row - startRow > 1) {
                    rows[startRow].cells[col].rowSpan = row - startRow;
                    for (let i = startRow + 1; i < row; i++) {
                        rows[i].cells[col].style.display = 'none';
                    }
                }
                if (row < rowCount) {
                    startRow = row;
                    value = rows[row].cells[col].innerText;
                }
            }
        }
    }
}

// Ajouter des écouteurs d'événements pour les boutons de téléchargement
document.getElementById('download-xlsx').addEventListener('click', downloadXLSX);
document.getElementById('download-csv').addEventListener('click', downloadCSV);
document.getElementById('download-pdf').addEventListener('click', downloadPDF);



function downloadXLSX() {
    if (!filteredTableData || filteredTableData.length === 0) {
        alert("No data selected.");
        return;
    }

    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet([]);

    // Ajouter les en-têtes avec fusion
    const columns = tableData.columns; // Les colonnes hiérarchiques
    const levels = columns.length > 0 ? columns[0].length : 0;

    let rowOffset = 0; // Pour suivre l'offset des lignes
    ws['!merges'] = []; // Initialiser les fusions

    for (let level = 0; level < levels; level++) {
        const headerRow = [];
        let previousValue = null;
        let colspanStartIndex = 0;

        columns.forEach((col, index) => {
            const currentValue = col[level];

            if (currentValue === previousValue) {
                // Continue la fusion pour les valeurs identiques
                return;
            } else {
                // Si une valeur change, ajouter une fusion si nécessaire
                if (previousValue !== null && index - colspanStartIndex > 1) {
                    ws['!merges'].push({
                        s: { r: rowOffset, c: colspanStartIndex },
                        e: { r: rowOffset, c: index - 1 }
                    });
                }

                // Ajouter la valeur actuelle et mettre à jour les indices
                headerRow.push(currentValue || '');
                previousValue = currentValue;
                colspanStartIndex = index;
            }

            // Dernière cellule de la ligne
            if (index === columns.length - 1 && index - colspanStartIndex > 0) {
                ws['!merges'].push({
                    s: { r: rowOffset, c: colspanStartIndex },
                    e: { r: rowOffset, c: index }
                });
            }
        });

        // Ajouter la ligne d'en-têtes au tableau
        XLSX.utils.sheet_add_aoa(ws, [headerRow], { origin: rowOffset });
        rowOffset++;
    }

    // Ajouter les données du tableau
    filteredTableData.forEach(row => {
        const rowData = tableData.columns.map(col => {
            const key = Array.isArray(col) ? col.join(' ') : col;
            return row[key];
        });

        XLSX.utils.sheet_add_aoa(ws, [rowData], { origin: rowOffset });
        rowOffset++;
    });

    // Ajouter la feuille de calcul au classeur
    XLSX.utils.book_append_sheet(wb, ws, 'Data');

    // Télécharger le fichier Excel
    XLSX.writeFile(wb, 'donnees_filtrees.xlsx');
}


function downloadCSV() {
    if (!filteredTableData || filteredTableData.length === 0) {
        alert("Aucune variable sélectionnée");
        return;
    }

    // Gérer les colonnes hiérarchiques
    const columns = tableData.columns; // Colonnes hiérarchiques
    const levels = columns.length > 0 ? columns[0].length : 0;

    // Construire les en-têtes hiérarchiques
    const headerRows = Array.from({ length: levels }, () => Array(columns.length).fill(''));
    columns.forEach((col, colIndex) => {
        col.forEach((value, levelIndex) => {
            headerRows[levelIndex][colIndex] = value || '';
        });
    });

    // Ajouter les données
    const dataRows = filteredTableData.map(row =>
        columns.map(col => {
            const key = Array.isArray(col) ? col.join(' ') : col; // Normaliser la clé de colonne
            return row[key] || ''; // Remplace undefined par une chaîne vide
        })
    );

    // Combiner les lignes d'en-têtes et de données pour créer le CSV
    const csvContent = [
        ...headerRows.map(row => row.map(value => {
            // Échapper les valeurs contenant des virgules, guillemets ou nouvelles lignes
            if (typeof value === 'string' && (value.includes(',') || value.includes('"') || value.includes('\n'))) {
                return `"${value.replace(/"/g, '""')}"`; // Échapper les guillemets
            }
            return value;
        }).join(',')), // Ajouter chaque ligne d'en-tête
        ...dataRows.map(row => row.map(value => {
            if (typeof value === 'string' && (value.includes(',') || value.includes('"') || value.includes('\n'))) {
                return `"${value.replace(/"/g, '""')}"`; // Échapper les guillemets
            }
            return value;
        }).join(',')) // Ajouter chaque ligne de données
    ].join('\n');

    // Créer un fichier blob et déclencher le téléchargement
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'donnees_filtrees.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}




function downloadPDF() {
    if (!filteredTableData || filteredTableData.length === 0) {
        alert("Aucune variable sélectionnée");
        return;
    }
    const { jsPDF } = window.jspdf;

    // Calcul de la largeur totale
    const pageWidth = 210; // Largeur d'une page A4 en mm
    const columnWidths = tableData.columns.map(() => 30); // Largeur par défaut des colonnes
    const totalWidth = columnWidths.reduce((sum, width) => sum + width, 0);

    // Choix de l'orientation
    const orientation = totalWidth > pageWidth ? 'landscape' : 'portrait';
    const doc = new jsPDF({ orientation });

    // Calcul de la largeur ajustée des colonnes
    const availablePageWidth = orientation === 'landscape' ? 297 - 20 : 210 - 20; // Largeur en paysage ou portrait, moins les marges
    const adjustedColumnWidths = columnWidths.map(width =>
        (width / totalWidth) * availablePageWidth
    );

    // Titre du PDF
    const pdfTitleElement = document.getElementById('pdf-title');
    const pdfTitle = pdfTitleElement ? pdfTitleElement.textContent.trim() : 'Données Filtrées';
    doc.setFontSize(16);
    doc.text(pdfTitle, 10, 15);

    // Préparer les données du tableau
    const columns = tableData.columns;
    const bodyRows = filteredTableData.map(row =>
        columns.map(col => {
            const key = Array.isArray(col) ? col.join(' ') : col;
            const value = row[key] || '';
            return value.length > 50 ? `${value.substring(0, 47)}...` : value; // Tronquer si nécessaire
        })
    );

    // Générer le tableau avec autoTable
    doc.autoTable({
        startY: 25,
        head: [columns],
        body: bodyRows,
        theme: 'grid',
        headStyles: { fillColor: [0, 107, 69], textColor: [255, 153, 0], fontStyle: 'bold' },
        bodyStyles: { fontSize: 10, cellPadding: 2, halign: 'center' },
        alternateRowStyles: { fillColor: [245, 245, 245] },
        margin: { left: 10, right: 10 },
        styles: {
            overflow: 'linebreak',
            cellWidth: 'auto',
        },
        columnStyles: columns.reduce((acc, _, index) => {
            acc[index] = { cellWidth: adjustedColumnWidths[index] || 'auto' };
            return acc;
        }, {})
    });

    // Télécharger le PDF
    const filename = orientation === 'landscape' ? 'donnees_filtrees_landscape.pdf' : 'donnees_filtrees_portrait.pdf';
    doc.save(filename);
}





