
document.addEventListener('DOMContentLoaded', function () {
    const statisticsTableBody = document.querySelector('#statisticsTable tbody');

    async function fetchAndUpdateStatistics() {
        try {
            const response = await fetch('/api/statistics');
            if (!response.ok) {
                throw new Error('Failed to fetch statistics');
            }

            const statistics = await response.json();

            statisticsTableBody.innerHTML = '';

            statistics.forEach(stat => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${stat.algorithm}</td>
                    <td>${stat.total_records}</td>
                    <td>${stat.average_steps}</td>
                    <td>${stat.average_path_length}</td>
                    <td>${stat.average_time}</td>
                    <td>${stat.average_weight}</td>
                `;
                statisticsTableBody.appendChild(row);
            });
        } catch (error) {
            console.error('Error fetching statistics:', error);
        }
    }

    fetchAndUpdateStatistics();

    setInterval(fetchAndUpdateStatistics, 5000);
});
