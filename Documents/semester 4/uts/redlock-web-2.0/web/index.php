<!DOCTYPE html>
<html>
<head>
	<title>Redlock User Database</title>
	<style>
		table {
			font-family: Arial, sans-serif;
			border-collapse: collapse;
			width: 100%;
		}

		td, th {
			border: 1px solid #ddd;
			padding: 8px;
		}

		tr:nth-child(even){background-color: #f2f2f2;}

		tr:hover {background-color: #ddd;}

		th {
			padding-top: 12px;
			padding-bottom: 12px;
			text-align: left;
			background-color: #4CAF50;
			color: white;
		}
	</style>
</head>
<body>
	<h1>Redlock User Database</h1>
	<table>
		<thead>
			<tr>
				<th>ID</th>
				<th>Nama</th>
				<th>Alamat</th>
				<th>Jabatan</th>
			</tr>
		</thead>
		<tbody>
			<?php
			// membuat koneksi ke database
            $servername = "mysql_db";
            $username = "root";
            $password = "root";
            $dbname = "Redlock";
    
            // Membuat koneksi ke database
            $conn = new mysqli($servername, $username, $password, $dbname);
    
            // Mengecek apakah koneksi berhasil
            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }

			$sql = "SELECT * FROM users";
			$result = $conn->query($sql);

			if ($result->num_rows > 0) {
			    // output data of each row
			    while($row = $result->fetch_assoc()) {
			        echo "<tr><td>" . $row["ID"]. "</td><td>" . $row["Nama"]. "</td><td>" . $row["Alamat"]. "</td><td>" . $row["Jabatan"]. "</td></tr>";
			    }
			} else {
			    echo "0 results";
			}
			$conn->close();
			?>
		</tbody>
	</table>
</body>
</html>

