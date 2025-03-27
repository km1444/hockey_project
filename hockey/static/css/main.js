const table = document.querySelector('table');
let colIndex = -1
table.onclick = function(e) {
    if(e.target.tagName != 'TH') return
    let th = e.target
    sortTable(th.cellIndex, th.getAttribute('data-type'), colIndex === th.cellIndex)
    colIndex = (colIndex === th.cellIndex) ? -1 : th.cellIndex;
};


function sortTable(colNum, type, isSorted) {
    let tbody = table.querySelector('tbody')
    for (let elem of table.querySelectorAll('.table-warning')) {
        elem.removeAttribute("class")
    }
    let rowsArray = Array.from(tbody.rows)
    let compare;
    switch(type) {
        case 'number':
            compare = function(rowA, rowB) {
                rowA.cells[colNum].setAttribute('class', "table-warning");
                rowB.cells[colNum].setAttribute('class', "table-warning");
                return rowB.cells[colNum].innerHTML - rowA.cells[colNum].innerHTML
            }
            break;
        case 'string':
            compare = function(rowA, rowB) {
                return rowA.cells[colNum].innerText > rowB.cells[colNum].innerText ? 1 : -1
            }
            break;
    }
    // rowsArray.sort(compare)
    if (isSorted) rowsArray.sort(compare).reverse()
        else rowsArray.sort(compare)
    
    tbody.append(...rowsArray)
}
// const table = document.querySelector('table');
// let colIndex = -1;

// const sortTable = function (index, type, isSorted) {
//     const tbody = table.querySelector('tbody');

//     const compare = function(rowA, rowB) {
//         const rowDataA = rowA.cells[index].innerHTML;
//         const rowDataB = rowB.cells[index].innerHTML;

//         switch (type) {
//             case 'number':
//                 return rowDataA - rowDataB;
//                 break;
//             case 'string':
//                 if (rowDataA < rowDataB) return -1;
//                 else if(rowDataA > rowDataB) return 1;
//                 return 0;
//                 break;
//         }
//     }

//     let rows = [].slice.call(tbody.rows);

//     rows.sort(compare);

//     if (isSorted) rows.reverse();

//     table.removeChild(tbody);

//     for (let i = 0; i < rows.length; i++) {
//         tbody.appendChild(rows[i]);
//     }

//     table.appendChild(tbody);
// }

// table.addEventListener('click', (e) => {
//    const el = e.target;
//    if (el.nodeName !== 'TH') return;

//    const index = el.cellIndex; 
//    const type = el.getAttribute('data-type');

//    sortTable(index, type, colIndex === index);
//    colIndex = (colIndex === index) ? -1 : index;
// });
