const draggableItems = document.querySelectorAll('.draggable-item');
const droppableAreaRows = document.getElementById('droppable-area-rows');
const droppableAreaCols = document.getElementById('droppable-area-cols');
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

function handleDragStart(event) {
    event.dataTransfer.setData('text/plain', event.target.dataset.column);
}

function handleDragOver(event) {
    event.preventDefault();
}

function handleDrop(event, type) {
    event.preventDefault();
    //const column = event.dataTransfer.getData('text/plain');
    //console.table(column,type);
    
    const column = event.dataTransfer.getData('text/plain');

    if (type === 'row' && !rowColumns.includes(column)) {
        rowColumns.push(column);
        addColumnToArea(column, droppableAreaRows, rowColumns, type);
    } 
    
    else if (type === 'col') {

        // Vérifie si une colonne est déjà présente dans `colColumns`
       if (!colColumns.includes(column)) {
            colColumns.push(column);
            addColumnToArea(column, droppableAreaCols, colColumns, type);
        } else {
            alert("Vous ne pouvez déposer une seule varaible en colonne");
        }
    }
    sendColumnsToServer();
    console.table(colColumns.length);
}


function addColumnToArea(column, area, columnList, type) {
    const newItem = document.createElement('div');
    newItem.classList.add('draggable-item');
    newItem.textContent = column;
    newItem.setAttribute('draggable', 'true');
    newItem.setAttribute('data-column', column);
    newItem.addEventListener('dragstart', handleDragStart);

    newItem.addEventListener('click', function () {
        area.removeChild(newItem);
        columnList.splice(columnList.indexOf(column), 1);
        sendColumnsToServer();
    });

    area.appendChild(newItem);
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
            value_column: 'valeur'
        })
    })
    .then(response => response.json())
    .then(data => {
        // Reformatez tableData pour qu'il soit un tableau d'objets
        tableData = data.data.map(row => {
            const rowData = {};
            data.columns.forEach((col, index) => {
                rowData[col.join(' ')] = row[index];  // Combine les noms de colonnes multi-niveaux
            });
            return rowData;
        });

        tableData.columns = data.columns; // Stockez les colonnes
        filteredTableData = tableData;
        generateTable(data);
        generateFilters();
    })
    .catch(error => console.error('Erreur:', error));
}






function generateTable(data) {
    tableContainer.innerHTML = '';

    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    // Créer les en-têtes hiérarchiques pour les colonnes avec fusion
    const columns = data.columns;
    const levels = columns.length > 0 ? columns[0].length : 0;

    for (let level = 0; level < levels; level++) {
        const headerRow = document.createElement('tr');
        let previousValue = null;
        let colspan = 0;

        columns.forEach((col, index) => {
            const currentValue = col[level];

            if (currentValue === previousValue) {
                colspan += 1;  // Incrémente le colspan pour les valeurs identiques
            } else {
                // Si la valeur change, appliquez le colspan et réinitialisez-le
                if (colspan > 0) {
                    headerRow.lastChild.setAttribute('colspan', colspan);
                }
                const th = document.createElement('th');
                th.textContent = currentValue || '';
                headerRow.appendChild(th);
                previousValue = currentValue;
                colspan = 1;  // Réinitialise colspan pour la nouvelle valeur
            }

            // Pour la dernière cellule de la ligne, appliquez le colspan
            if (index === columns.length - 1 && colspan > 1) {
                headerRow.lastChild.setAttribute('colspan', colspan);
            }
        });
        thead.appendChild(headerRow);
    }

    // Génération du corps du tableau en respectant l’ordre des colonnes
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
        filterTitle.textContent = `Filtrer par ${col}`;
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

function downloadXLSX() {
    if (!filteredTableData || filteredTableData.length === 0) {
        alert("No data selected.");
        return;
    }

    // Créer un workbook avec SheetJS
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(filteredTableData);
    XLSX.utils.book_append_sheet(wb, ws, 'Data');

    // Télécharger le fichier
    XLSX.writeFile(wb, 'donnees_filtrees.xlsx');
}

function downloadCSV() {
    if (!filteredTableData || filteredTableData.length === 0) {
        alert("Aucune variable selectionnée");
        return;
    }

    const headers = Object.keys(filteredTableData[0]);
    const rows = filteredTableData.map(row => headers.map(header => row[header]));

    // Construire le contenu CSV
    const csvContent = [
        headers.join(','),    // Ajouter l'en-tête
        ...rows.map(row => row.join(','))   // Ajouter les lignes
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
