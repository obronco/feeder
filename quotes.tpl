<html>
    <head>
    <style>
    table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }
    td, th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }
    tr:nth-child(even) {
        background-color: #dddddd;
    }
    </style>
    </head>
    <body>
    <p></p>
    <b>Last update: {{ts}}</b>
    <p></p>
    <table>
        <tr>
        <th>Classe</th>
        <th>Ativo</th>
        <th>Ult</th>
        <th>OCp</th>
        <th>OVd</th>
        <th>Fech D-0</th>
        <th>Fech D-1</th>
        <th>Min</th>
        <th>Max</th>
        <th>Abe</th>
        </tr>
        % for row in quotes:
            <tr>
            % for cell in row:
                <td>{{cell}}</td>
            % end
            </tr>
        % end
    </table>
    </body>
</html>