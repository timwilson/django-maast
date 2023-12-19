document.addEventListener('DOMContentLoaded', function () {
    const personId = document.querySelector('[data-person-id]').dataset.personId;
    loadScoresTable(personId);  // Load the scores by default

    document.getElementById('btnScores').addEventListener('click', function (event) {
        event.preventDefault();
        setActiveTab(this);
        toggleTables('scores');
        loadScoresTable(personId);
    });

    document.getElementById('btnStateRecords').addEventListener('click', function (event) {
        event.preventDefault();
        setActiveTab(this);
        toggleTables('stateRecords');
        loadStateRecordsTable(personId);
    });

    document.getElementById('btnPodiums').addEventListener('click', function (event) {
        event.preventDefault();
        setActiveTab(this);
        toggleTables('podiums');
        loadPodiumsTable(personId);
    });

    function setActiveTab(activeTabElement) {
        // Define the classes for active and inactive states
        const activeClasses = ['border-nfaaorange', 'text-nfaaorange'];
        const inactiveClasses = ['border-transparent', 'text-gray-500'];

        // Reset classes on all tabs to inactive state
        document.querySelectorAll('nav > a').forEach(tab => {
            tab.classList.remove(...activeClasses);
            tab.classList.add(...inactiveClasses);
        });

        // Set the clicked tab to active state
        activeTabElement.classList.remove(...inactiveClasses);
        activeTabElement.classList.add(...activeClasses);
    }

    document.getElementById('current-tab').addEventListener('change', function () {
        const selectedTab = this.value;
        switch (selectedTab) {
            case 'scores':
                setActiveTab(document.getElementById('btnScores'));
                toggleTables('scores');
                loadScoresTable(personId);
                break;
            case 'stateRecords':
                setActiveTab(document.getElementById('btnStateRecords'));
                toggleTables('stateRecords');
                loadStateRecordsTable(personId);
                break;
            case 'podiums':
                setActiveTab(document.getElementById('btnPodiums'));
                toggleTables('podiums');
                loadPodiumsTable(personId);
                break;
        }
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
                {
                    target: 0, // Division
                    render: function (data, type, row) {
                        let q_division = '?age_division=' + encodeURIComponent(row.age_division) +
                            '&gender=' + encodeURIComponent(row.gender) +
                            '&equipment_class=' + encodeURIComponent(row.equipment_class)
                        return '<a href="/scores/' + row.round_id + q_division + '" class="underline decoration-dotted decoration-from-font underline-offset-4 hover:decoration-solid hover:decoration-nfaaorange">' + row.division + '</a>';
                    }
                },
                {
                    targets: 1, // Score
                    className: "text-sm",
                },
                {
                    target: 3, // Event
                    render: function (data, type, row) {
                        return '<a href="/event/' + row.event_id + '" class="underline decoration-dotted decoration-from-font underline-offset-4 hover:decoration-solid hover:decoration-nfaaorange">' + data + '</a>';
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
                        return '<a href="/records/' + row.round_id + '" class="underline decoration-dotted decoration-from-font underline-offset-4 hover:decoration-solid hover:decoration-nfaaorange">' + data + '</a>';
                    }
                },
                {
                    target: 1, // Division
                    render: function (data, type, row) {
                        let division = '?age_division=' + encodeURIComponent(row.age_division) +
                            '&gender=' + encodeURIComponent(row.gender) +
                            '&equipment_class=' + encodeURIComponent(row.equipment_class)
                        return '<a href="/scores/' + row.round_id + division + '" class="underline decoration-dotted decoration-from-font underline-offset-4 hover:decoration-solid hover:decoration-nfaaorange">' + row.gender + ' ' + row.equipment_class + '</a>';
                    }
                },
                {
                    targets: 2, // Score
                    className: "text-sm",
                },
                {
                    targets: 4, // Event
                    render: function (data, type, row) {
                        return '<a href="/event/' + row.event_id + '" class="underline decoration-dotted decoration-from-font underline-offset-4 hover:decoration-solid hover:decoration-nfaaorange">' + data + '</a>';
                    }
                }
            ],
            rowGroup: {
                dataSrc: "age_division"
            },
            language: {
                emptyTable: "No state records to show"
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
                    render: function (data) {
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
                        return '<a href="/event/' + row.event_id + '" class="underline decoration-dotted decoration-from-font underline-offset-4 hover:decoration-solid hover:decoration-nfaaorange">' + data + '</a>';
                    }
                }
            ],
            rowGroup: {
                dataSrc: "division"
            },
            language: {
                emptyTable: "No podium finishes to show"
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
