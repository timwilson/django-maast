document.addEventListener('DOMContentLoaded', function () {
    const personId = document.querySelector('[data-person-id]').dataset.personId;
    loadScoresTable(personId);  // Load the scores by default

    document.getElementById('btnScores').addEventListener('click', function () {
        toggleTables('scores');
        loadScoresTable(personId);
    });
    document.getElementById('btnStateRecords').addEventListener('click', function () {
        toggleTables('stateRecords');
        loadStateRecordsTable(personId);
    });
    document.getElementById('btnPodiums').addEventListener('click', function () {
        toggleTables('podiums');
        loadPodiumsTable(personId);
    });

    function toggleTables(tableToShow) {
        // Cache the jQuery objects
        let scoresTableContainer = $('#scoresTableContainer');
        let stateRecordsTableContainer = $('#stateRecordsTableContainer');
        let podiumsTableContainer = $('#podiumsTableContainer');

        // Hide all the table containers
        scoresTableContainer.hide();
        stateRecordsTableContainer.hide();
        podiumsTableContainer.hide();

        // Show the selected table container
        switch (tableToShow) {
            case 'scores':
                scoresTableContainer.show();
                break;
            case 'stateRecords':
                stateRecordsTableContainer.show();
                break;
            case 'podiums':
                podiumsTableContainer.show();
                break;
        }
    }

    function loadScoresTable(personId) {
        let url = "/api/scores/" + personId;
        let columnConfig = [
            {title: "Division", data: "division"},
            {title: "Score", data: "pretty_score"},
            {title: "Date", data: "score_date"},
            {title: "Event", data: "event_name"},
            {title: "Location", data: "event_location"},
        ];
        let tableOptions = {
            columnDefs: [
                {targets: [0, 1, 2, 3, 4], className: "text-sm"},
                {target: 0, // Division
                    render: function ( data, type, row ) {
                    let q_division = '?age_division='+encodeURIComponent(row.age_division)+
                        '&gender='+encodeURIComponent(row.gender)+
                        '&equipment_class='+encodeURIComponent(row.equipment_class)
                    return '<a href="/scores/'+row.round_id+q_division+'">'+row.division+'</a>';
                    }
                },
                {
                    targets: 1, // Score
                    className: "text-sm text-center",
                },
                {target: 3, // Event
                    render: function ( data, type, row ) {
                        return '<a href="/event/' + row.event_id + '">' + data + '</a>';
                    }
                },
            ],
            rowGroup: {
                dataSrc: "round"
            },
            responsive: true,
            fixedHeader: true,
            paging: true,
            pageLength: 50,
            lengthChange: false,
            ordering: false,
            info: true,
            searching: true,
            preDrawCallback: function (settings) {
                const api = new $.fn.dataTable.Api(settings);
                const pagination = $(api.table().container()).find('.dataTables_paginate');
                pagination.toggle(api.page.info().pages > 1);
            },
        };
        loadDataAndInitializeTable(url, columnConfig, tableOptions, '#scoresTable');
    }

    function loadStateRecordsTable(personId) {
        let url = "/api/records/" + personId;
        let columnConfig = [
            {title: "Round", data: "round"},
            {title: "Division", data: "division"},
            {title: "Score", data: "score"},
            {title: "Date", data: "score_date"},
            {title: "Event", data: "event_name"},
            {title: "Location", data: "event_location"},
        ];
        let tableOptions = {
            columnDefs: [
                {targets: [0, 1, 2, 3, 4, 5], className: "text-sm"},
                {
                    targets: 0, // Round
                    render: function (data, type, row) {
                        return '<a href="/records/' + row.round_id + '">' + data + '</a>';
                    }
                },
                {
                    targets: 2, // Score
                    className: "text-sm text-center",
                },
                {
                    targets: 4, // Event
                    render: function (data, type, row) {
                        return '<a href="/event/' + row.event_id + '">' + data + '</a>';
                    }
                }
            ],
            rowGroup: {
                dataSrc: "age_division"
            },
            responsive: true,
            fixedHeader: true,
            paging: true,
            pageLength: 50,
            lengthChange: false,
            ordering: false,
            info: true,
            searching: true,
            preDrawCallback: function (settings) {
                const api = new $.fn.dataTable.Api(settings);
                const pagination = $(api.table().container()).find('.dataTables_paginate');
                pagination.toggle(api.page.info().pages > 1);
            },
        };
        loadDataAndInitializeTable(url, columnConfig, tableOptions, '#stateRecordsTable');
    }

    function loadPodiumsTable(personId) {
        let url = "/api/podiums/" + personId;
        let columnConfig = [
            {title: "Place", data: "place"},
            {title: "Event", data: "event_name"},
            {title: "Date", data: "event_date"},
            {title: "Location", data: "event_location"},
        ];
        let tableOptions = {
            columnDefs: [
                {targets: [0, 1, 2, 3], className: "text-sm"},
                {
                    targets: 0, // Place
                    render: function (data, type, row) {
                        switch (data) {
                            case 1:
                                return '🥇';
                            case 2:
                                return '🥈';
                            case 3:
                                return '🥉';
                            default:
                                return data;
                        }
                    },
                },
                {
                    targets: 1, // Event
                    render: function (data, type, row) {
                        return '<a href="/event/' + row.event_id + '">' + data + '</a>';
                    }
                }
            ],
            rowGroup: {
                dataSrc: "division"
            },
            responsive: true,
            fixedHeader: true,
            paging: true,
            pageLength: 50,
            lengthChange: false,
            ordering: false,
            info: true,
            searching: true,
            preDrawCallback: function (settings) {
                const api = new $.fn.dataTable.Api(settings);
                const pagination = $(api.table().container()).find('.dataTables_paginate');
                pagination.toggle(api.page.info().pages > 1);
            },
        };
        loadDataAndInitializeTable(url, columnConfig, tableOptions, '#podiumsTable');
    }

    function loadDataAndInitializeTable(url, columnConfig, tableOptions, tableSelector) {
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function (data) {
                let dataTable = $(tableSelector);

                // Destroy existing DataTable
                if ($.fn.DataTable.isDataTable(dataTable)) {
                    dataTable.DataTable().clear().destroy();
                }

                // Clear the table content
                dataTable.empty();

                // Initialize new DataTable
                dataTable.DataTable($.extend({}, {
                    data: data,
                    columns: columnConfig,
                }, tableOptions));

                // Modify table classes
                // I don't think this renders properly because it's added dynamically after
                // the table is created. The tailwind system doesn't see it, so it's not rendered.
                dataTable.find('h1').addClass('text-lg');
            },
            error: function (error) {
                console.error("Error loading data: ", error);
            }
        });
    }
});
