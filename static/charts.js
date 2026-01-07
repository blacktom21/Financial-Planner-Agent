function renderExpenseChart(expenses) {
    const ctx = document.getElementById("expenseChart");

    const labels = Object.keys(expenses);
    const values = Object.values(expenses);

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    "#60a5fa",
                    "#34d399",
                    "#fbbf24",
                    "#f87171",
                    "#a78bfa"
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
}
