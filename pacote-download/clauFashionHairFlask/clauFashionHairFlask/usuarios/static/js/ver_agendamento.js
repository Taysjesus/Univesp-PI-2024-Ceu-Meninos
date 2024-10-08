//Função javaScript para ordenar a lista de agendamentos por data e hora
document.addEventListener('DOMContentLoaded', function() {
            const list = document.getElementById('agendamentos-list');
            const items = Array.from(list.getElementsByTagName('li'));

            items.sort((a, b) => {
                const dateA = new Date(a.textContent.split(' - ')[1].replace(' às ', ' '));
                const dateB = new Date(b.textContent.split(' - ')[1].replace(' às ', ' '));
                return dateA - dateB;
            });

            items.forEach(item => list.appendChild(item));
        });


