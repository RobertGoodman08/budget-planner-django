const searchField = document.querySelector("#searchField")
const noResults = document.querySelector(".no-results");
const tableOutput = document.querySelector(".table-output");
tableOutput.style.display = "none";

const paginationContainer = document.querySelector(".pagination-container");
const appTable = document.querySelector("#app-table");
const tbody = document.querySelector(".table-body");

searchField.addEventListener('keyup', (e) => {


    const searchValue = e.target.value;


    if (searchValue.trim().length > 0) {
        console.log("searchValue", searchValue)

        paginationContainer.style.display = "none";
        tbody.innerHTML = "";
        fetch("/income/search-income/", {
            body: JSON.stringify({searchText: searchValue}),
            method: "POST",

        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data)
            appTable.style.display = "none";
            tableOutput.style.display = "block";


            if (data.length === 0) {
                 noResults.style.display = "block";
                 tableOutput.style.display = "none";
            }else{
                noResults.style.display = "none";
                data.forEach((item) => {
                    tbody.innerHTML += `
                        <tr>
                            <td>${item.id}</td>
                            <td><a href="/income/income_details/${item.id}/">${item.amount}</a></td>
                            <td><a href="/income/income_details/${item.id}/">${item.source}</a></td>
                            <td><a href="/income/income_details/${item.id}/">${item.description}</a></td>
                            <td>${item.date}</td>
                            <td><span class="badge-dot  mr-1"></span><a href="/income/edit-income/${item.id}/"><b>Редактировать</b></a></td>
                            <td><span class="badge-dot  mr-1"></span><a href="/income/income-delete/${item.id}/"><b class="btn btn-danger">Удалите</b></a></td>
                        </tr>
                    `;
                });
            }

        });
    } else{
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }

});
