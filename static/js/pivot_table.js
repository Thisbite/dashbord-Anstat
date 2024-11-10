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
    const column = event.dataTransfer.getData('text/plain');

    if (type === 'row' && !rowColumns.includes(column)) {
        rowColumns.push(column);
        addColumnToArea(column, droppableAreaRows, rowColumns, type);
    } else if (type === 'col' && !colColumns.includes(column)) {
        colColumns.push(column);
        addColumnToArea(column, droppableAreaCols, colColumns, type);
    }

    sendColumnsToServer();
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


function generateFilters() {
    filterContainer.innerHTML = '';

    const allColumns = [...rowColumns, ...colColumns];
    console.log("Columns for filters:", allColumns);

    allColumns.forEach(col => {
        const label = document.createElement('label');
        label.textContent = `Filtrer par ${col}:`;
        const select = document.createElement('select');
        select.setAttribute('data-column', col);

        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Tous';
        select.appendChild(defaultOption);

        // Assurez-vous d'avoir le bon format de clé
        const colKey = Array.isArray(col) ? col.join(' ') : col;
        const uniqueValues = [...new Set(tableData.map(row => row[colKey]))];
        console.log(`Unique values for ${colKey}:`, uniqueValues);

        uniqueValues.forEach(value => {
            if (value !== undefined) {  // Ignore les valeurs undefined
                const option = document.createElement('option');
                option.value = value;
                option.textContent = value;
                select.appendChild(option);
            }
        });

        select.addEventListener('change', applyFilters);
        filterContainer.appendChild(label);
        filterContainer.appendChild(select);
    });
}



function applyFilters() {
    filteredTableData = [...tableData];
    console.log("Applying filters...");

    const selects = filterContainer.querySelectorAll('select');
    selects.forEach(select => {
        const column = select.getAttribute('data-column');
        const value = select.value;

        if (value) {
            const colKey = Array.isArray(column) ? column.join(' ') : column;
            console.log(`Filtering on ${colKey} with value:`, value);

            filteredTableData = filteredTableData.filter(row => {
                const rowValue = row[colKey];
                console.log(`Row value for ${colKey}:`, rowValue);
                return rowValue == value;
            });
        }
    });

    // Conservez la structure des colonnes en passant `tableData.columns`
    generateTable({
        columns: tableData.columns,
        data: filteredTableData.map(row => {
            return tableData.columns.map(col => {
                const key = col.join(' ');
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
