document.addEventListener('DOMContentLoaded', function () {
    // Function to update the table with the received data
    function updateTable(data) {
        // Log existing table IDs
        console.log('Existing Table IDs:', Array.from(document.querySelectorAll('table')).map(table => table.id));

        // Assuming you have a table with id 'resultsTable'
        var table = document.getElementById('resultsTable');

        if (!table) {
            console.error('Table with ID "resultsTable" not found.');
            return;
        }

        if (!data || data.length === 0) {
            console.error('No data to display.');
            return;
        }

        // Clear existing rows in the table
        table.innerHTML = '';

        // Create header row
        var headerRow = table.createTHead().insertRow(0);
        var headerCell1 = headerRow.insertCell(0);
        var headerCell2 = headerRow.insertCell(1);

        // Set header cell values
        headerCell1.textContent = 'Country Name';
        headerCell2.textContent = 'Flag Image URL';  // Adjust headers based on your data structure

        // Create rows with data
        for (var i = 0; i < data.length; i++) {
            var row = table.insertRow(i + 1);  // Start from 1 to skip header row
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);

            // Set cell values based on your data structure
            cell1.textContent = data[i].country_name;
            cell2.textContent = data[i].flag_image_url;
        }
    }

    var form = document.getElementById('myForm');
    var subTopicSelection = document.getElementById('sub_topic_selection');
    var continentOptions = document.getElementById('continent_options');
    var populationOptions = document.getElementById('population_options');
    var subSubTopicContinent = document.getElementById('sub_sub_topic_continent');
    var subSubTopicPopulation = document.getElementById('sub_sub_topic_population');

    function updateSubTopicSelection() {
        subTopicSelection.style.display = document.getElementById('detailed_query').checked ? 'block' : 'none';

        // Reset the sub-sub-topic value when changing the sub-topic
        subSubTopicContinent.value = '';
        subSubTopicPopulation.value = '';

        continentOptions.style.display = 'none';
        populationOptions.style.display = 'none';

        var subTopicValue = document.getElementById('sub_topic').value;
        if (subTopicValue === 'continent') {
            continentOptions.style.display = 'block';
            subSubTopicContinent.setAttribute('required', 'true');
            subSubTopicPopulation.removeAttribute('required');
        } else if (subTopicValue === 'population') {
            populationOptions.style.display = 'block';
            subSubTopicPopulation.setAttribute('required', 'true');
            subSubTopicContinent.removeAttribute('required');
        } else {
            subSubTopicContinent.removeAttribute('required');
            subSubTopicPopulation.removeAttribute('required');
        }
    }

    // Check if the checkbox is initially checked
    updateSubTopicSelection();

    document.getElementById('detailed_query').addEventListener('change', updateSubTopicSelection);

    document.getElementById('sub_topic').addEventListener('change', function () {
        updateSubTopicSelection();
    });

    // Add an event listener to the form for submission
    form.addEventListener('submit', function (event) {
        // Log the selected values for debugging
        console.log('Form submitted!');
        console.log('Main Topic:', document.getElementById('topic').value);
        console.log('More Specific Topic:', document.getElementById('detailed_query').checked);

        var formData = new FormData(form);  // Create a FormData object

        if (document.getElementById('detailed_query').checked) {
            console.log('Sub-topic:', document.getElementById('sub_topic').value);

            if (document.getElementById('sub_topic').value === 'continent') {
                console.log('Sub-sub-topic (Continent):', subSubTopicContinent.value);
            }

            if (document.getElementById('sub_topic').value === 'population') {
                console.log('Sub-sub-topic (Population Size):', subSubTopicPopulation.value);
            }
        }

        // Append the additional data to the FormData object
        formData.append('sub_sub_topic_continent', subSubTopicContinent.value);
        formData.append('sub_sub_topic_population', subSubTopicPopulation.value);

        // Send the form data to the server using a fetch request
        fetch('/results', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Log the data for debugging
            console.log(data);
    
            // Update the table with the received data
            updateTable(data.data);  // Assuming 'data' contains the results
        })
        .catch(error => console.error('Error:', error));
    
        event.preventDefault();
    });
});
