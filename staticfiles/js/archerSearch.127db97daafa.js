// Archer search function for the _header.html template
$(document).ready(function () {
    $('#search').on('input', function () {
        var query = $(this).val();

        if (query.length >= 3) {
            $.ajax({
                url: '/api/search',
                data: {
                    name: query
                },
                success: function (data) {
                    $('#search-results').empty();
                    // Create an unordered list with Tailwind classes
                    var resultList = $('<ul class="list-none bg-white rounded-lg shadow-lg">');

                    $.each(data, function (i, person) {
                        // Create list item for each result with Tailwind classes
                        var listItem = $('<li class="px-4 py-1 hover:bg-gray-100">')
                            .append($('<a>')
                                .attr('href', '/profile/' + person.slug)
                                .text(person.full_name)
                            );

                        // Append list item to the unordered list
                        resultList.append(listItem);
                    });

                    // Append the entire list to the search-results div
                    $('#search-results').append(resultList);
                }
            });
        } else {
            $('#search-results').empty();
        }
    });
});