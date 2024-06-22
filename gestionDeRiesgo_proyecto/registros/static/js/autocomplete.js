document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('autocomplete-input');
    let currentSuggestions = [];
    let isDeleting = false;

    input.addEventListener('input', async function(event) {
        const query = input.value;

        // Detect if the user is deleting
        if (event.inputType === 'deleteContentBackward') {
            isDeleting = true;
        } else {
            isDeleting = false;
        }

        if (query.length < 1) {
            currentSuggestions = [];
            return;
        }

        // Only fetch suggestions if not deleting
        if (!isDeleting) {
            const response = await fetch(`/buscar_calles/?term=${query}`);
            const suggestions = await response.json();
            currentSuggestions = suggestions;

            // Only suggest if there's exactly one suggestion
            if (suggestions.length === 1) {
                const suggestion = suggestions[0].value;
                if (suggestion.toLowerCase().startsWith(query.toLowerCase())) {
                    input.value = suggestion;
                    input.setSelectionRange(query.length, suggestion.length);
                }
            }
        }
    });

    input.addEventListener('keydown', function(event) {
        if (event.key === 'Tab') {
            event.preventDefault();
            if (currentSuggestions.length === 1) {
                const suggestion = currentSuggestions[0].value;
                input.value = suggestion;
                input.setSelectionRange(suggestion.length, suggestion.length);
            }
        }
    });
});
