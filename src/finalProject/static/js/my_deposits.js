let currentSortColumn = null; // Coluna atualmente ordenada

function sortTable(columnIndex) {
    const table = document.querySelector("table tbody");
    const rows = Array.from(table.rows);

    // Seleciona o botão da coluna atual
    const currentBtn = document.querySelectorAll(".sort-btn")[columnIndex];

    // Define a direção inicial
    let sortOrder = "asc"; // Vamos iniciar com "asc" (para baixo)

    // Ordena as linhas da tabela
    rows.sort((a, b) => {
        const cellA = a.cells[columnIndex].textContent.trim();
        const cellB = b.cells[columnIndex].textContent.trim();

        if (!isNaN(cellA) && !isNaN(cellB)) {
            // Ordenação numérica
            return sortOrder === "asc" ? cellA - cellB : cellB - cellA;
        }

        // Ordenação alfabética
        return sortOrder === "asc"
            ? cellA.localeCompare(cellB)
            : cellB.localeCompare(cellA);
    });

    // Reanexa as linhas ordenadas na tabela
    rows.forEach(row => table.appendChild(row));

    // Atualiza o estado das setas
    document.querySelectorAll(".sort-btn").forEach((btn, index) => {
        btn.classList.remove("asc", "desc"); // Remove as classes de todas as colunas

        if (index === columnIndex) {
            // A seta clicada vai para baixo ("desc")
            btn.classList.add("desc");
        } else {
            // As setas das outras colunas vão para cima ("asc")
            btn.classList.add("asc");
        }
    });

    // Atualiza a coluna atual
    currentSortColumn = columnIndex;

}
