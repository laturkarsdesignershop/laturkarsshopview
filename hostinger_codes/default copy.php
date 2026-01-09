<?php
/**
 * default.php
 * Hostinger-safe version to display orders with filters and search.
 * Pagination and search fixed.
 */

// --------------------------
// CONFIGURATION
// --------------------------
$host = "auth-db788.hstgr.io";
$database = "u777474409_ltmobileview";
$user = "u777474409_laturkarsmv";
$password = "LaturkarsMV@1234";

// --------------------------
// DATABASE CONNECTION
// --------------------------
$conn = new mysqli($host, $user, $password, $database);
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);

// --------------------------
// HELPER FUNCTIONS
// --------------------------
function executeQuery($conn, $sql, $fetchAll = false, $fetchOne = false) {
    $result = $conn->query($sql);
    if ($result === false) return null;

    if ($result instanceof mysqli_result) {
        $data = [];
        while ($row = $result->fetch_assoc()) $data[] = $row;
        if ($fetchOne) return $data[0] ?? null;
        if ($fetchAll) return $data;
        return $data;
    } else {
        return ["affectedRows" => $conn->affected_rows];
    }
}

function convertDate($date) {
    $parts = explode("-", $date);
    return (count($parts) === 3) ? "{$parts[2]}-{$parts[1]}-{$parts[0]}" : $date;
}

// --------------------------
// GET/POST FILTERS
// --------------------------
$searchKeyword = $_POST['searchKeyword'] ?? $_GET['searchKeyword'] ?? "";
$filterKeyword = $_POST['filterKeyword'] ?? $_GET['filterKeyword'] ?? "";
$page = max(1, intval($_GET['page'] ?? 1));
$perPage = max(1, intval($_GET['per_page'] ?? 10));
$offset = ($page - 1) * $perPage;

$orders = [];
$totalFiltered = 0;

// --------------------------
// QUERY ORDERS
// --------------------------
if ($filterKeyword === "todaydeliveries") {
    $sql = "SELECT o.*, COALESCE(c.fullname,'Unknown') AS customer_name,
                   COALESCE(c.phone,'') AS customer_phone,
                   COALESCE(c.mobile,'') AS customer_mobile
            FROM tailor_order o
            LEFT JOIN tailor_customers c ON o.id_customers = c.id_customers
            WHERE o.delivery_date = CURDATE() AND o.status != 'Deleted'
            ORDER BY o.id_order DESC
            LIMIT $perPage OFFSET $offset";
    $orders = executeQuery($conn, $sql, true);

    $sqlCount = "SELECT COUNT(*) AS total FROM tailor_order WHERE delivery_date = CURDATE() AND status != 'Deleted'";
    $totalFiltered = intval(executeQuery($conn, $sqlCount, false, true)['total']);

} elseif ($filterKeyword === "todayorders") {
    $sql = "SELECT o.*, COALESCE(c.fullname,'Unknown') AS customer_name,
                   COALESCE(c.phone,'') AS customer_phone,
                   COALESCE(c.mobile,'') AS customer_mobile
            FROM tailor_order o
            LEFT JOIN tailor_customers c ON o.id_customers = c.id_customers
            WHERE o.order_date LIKE CONCAT(CURDATE(),'%') AND o.status != 'Deleted'
            ORDER BY o.id_order DESC
            LIMIT $perPage OFFSET $offset";
    $orders = executeQuery($conn, $sql, true);

    $sqlCount = "SELECT COUNT(*) AS total FROM tailor_order WHERE order_date LIKE CONCAT(CURDATE(),'%') AND status != 'Deleted'";
    $totalFiltered = intval(executeQuery($conn, $sqlCount, false, true)['total']);

} else {
    $kw = $conn->real_escape_string("%$searchKeyword%");
    $sqlCount = "SELECT COUNT(*) AS total FROM tailor_order WHERE id_order LIKE '$kw' AND status != 'Deleted'";
    $totalFiltered = intval(executeQuery($conn, $sqlCount, false, true)['total']);

    $sqlPaged = "SELECT o.*, COALESCE(c.fullname,'Unknown') AS customer_name,
                        COALESCE(c.phone,'') AS customer_phone,
                        COALESCE(c.mobile,'') AS customer_mobile
                 FROM tailor_order o
                 LEFT JOIN tailor_customers c ON o.id_customers = c.id_customers
                 WHERE o.id_order LIKE '$kw' AND o.status != 'Deleted'
                 ORDER BY o.id_order DESC
                 LIMIT $perPage OFFSET $offset";
    $orders = executeQuery($conn, $sqlPaged, true);
}

// --------------------------
// FETCH PRODUCTS & STAFF
// --------------------------
$orderIds = array_column($orders, 'id_order');
$orderProductMap = [];
$staffIds = [];
if ($orderIds) {
    $idsStr = implode(",", $orderIds);
    $sqlProducts = "SELECT * FROM tailor_products WHERE id_order IN ($idsStr)";
    $allProducts = executeQuery($conn, $sqlProducts, true) ?: [];

    foreach ($allProducts as $p) {
        $oid = $p['id_order'];
        $orderProductMap[$oid][] = $p;
        if (!empty($p['id_staff'])) $staffIds[] = $p['id_staff'];
        if (!empty($p['cutting_staff'])) $staffIds[] = $p['cutting_staff'];
    }
}

$staffMap = [];
if ($staffIds) {
    $staffIdsStr = implode(",", array_unique($staffIds));
    $sqlStaff = "SELECT id_staff, fullname FROM tailor_staff WHERE id_staff IN ($staffIdsStr) AND status != 'Deleted'";
    $staffData = executeQuery($conn, $sqlStaff, true) ?: [];
    foreach ($staffData as $s) $staffMap[$s['id_staff']] = $s['fullname'];
}

// Attach products & calculate balances
foreach ($orders as &$order) {
    $order['products'] = $orderProductMap[$order['id_order']] ?? [];
    $cBill = floatval($order['cloth_bill'] ?? 0);
    $sBill = floatval($order['stitching_bill'] ?? 0);
    $advPay = floatval($order['advance_payment'] ?? 0);
    $order['balAmt'] = round($cBill + $sBill - $advPay, 2);

    foreach ($order['products'] as &$p) {
        $p['p_stitching_staff'] = $staffMap[$p['id_staff']] ?? "-";
        $p['p_cutting_staff'] = $staffMap[$p['cutting_staff']] ?? "-";
        $status = strtolower($p['status'] ?? '');
        if (strpos($status,'cut')!==false) $p['jobstatus']='Cutting';
        elseif (strpos($status,'sew')!==false) $p['jobstatus']='Stitching';
        elseif (strpos($status,'waiting')!==false) $p['jobstatus']='Ready';
        elseif (strpos($status,'delivered')!==false || strpos($status,'new')!==false) $p['jobstatus']=strtoupper($status);
        else $p['jobstatus']=strtoupper($status);
    }
}

// Close DB connection
$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LaturkarsMV-Orders</title>
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 p-2 pb-32">

<h1 class="text-xl sm:text-2xl font-bold mb-2">Orders (<?php echo count($orders); ?>/<?php echo $totalFiltered; ?>)</h1>

<!-- Search & Filter -->
<form method="POST" class="mb-3 flex flex-col sm:flex-row sm:items-center sm:space-x-2 w-full max-w-xl">
    <input type="text" name="searchKeyword" placeholder="Search Order ID..." value="<?php echo htmlspecialchars($searchKeyword); ?>" 
           class="p-2 border rounded w-full sm:flex-1 mb-2 sm:mb-0">

    <select name="filterKeyword" onchange="this.form.submit()" class="p-2 border rounded w-full sm:w-auto">
        <option value="">Filter Orders</option>
        <?php foreach (['todaydeliveries','todayorders'] as $filter): ?>
            <option value="<?php echo $filter; ?>" <?php if($filterKeyword==$filter) echo 'selected'; ?>><?php echo ucfirst($filter); ?></option>
        <?php endforeach; ?>
    </select>

    <button type="submit" class="p-2 bg-blue-600 text-white rounded w-full sm:w-auto mt-2 sm:mt-0">Search</button>
</form>

<!-- Orders -->
<?php if ($orders): ?>
    <div class="space-y-3">
        <?php foreach ($orders as $o): ?>
            <div class="bg-white border rounded-lg shadow p-2 overflow-x-auto">
                <div class="grid grid-cols-2 gap-1 mb-1">
                    <div class="font-bold">Order: <?php echo $o['id_order']; ?></div>
                    <div class="flex flex-col sm:flex-row sm:justify-end gap-1">
                        <div class="px-1 py-[2px] bg-yellow-800 text-white text-sm rounded text-center">Pay Status: <?php echo $o['payment_status']; ?></div>
                        <div class="border rounded-md text-center px-1 py-[2px]">Bal Pay: Rs. <?php echo $o['balAmt']; ?></div>
                    </div>
                </div>

                <p class="font-semibold text-sm sm:text-base"><?php echo $o['customer_name']; ?></p>
                <p class="text-xs sm:text-sm text-gray-600"><?php echo $o['customer_mobile'] ?? ''; ?> <?php echo $o['customer_phone'] ?? ''; ?></p>
                <p class="text-xs sm:text-sm text-blue-700 mb-2 font-bold">Delivery: <?php echo isset($o['delivery_date']) ? convertDate($o['delivery_date']) : 'NONE'; ?></p>

                <!-- Products Table -->
                <div class="overflow-x-auto">
                    <div class="min-w-full grid grid-cols-4 gap-1 bg-gray-200 rounded-sm p-1 font-bold text-xs sm:text-sm">
                        <div>Item</div>
                        <div class="text-center">Cut Staff</div>
                        <div class="text-center">Stit Staff</div>
                        <div class="text-center">Status</div>
                    </div>
                    <?php foreach ($o['products'] as $idx => $itm): ?>
                        <div class="grid grid-cols-4 gap-1 p-1 bg-white border-b text-xs sm:text-sm">
                            <div><?php echo $idx+1; ?>. <?php echo ($itm['shirt_type'] ?? $itm['pant_type']) . ' x' . $itm['qty']; ?></div>
                            <div class="text-center"><?php echo $itm['p_cutting_staff']; ?></div>
                            <div class="text-center"><?php echo $itm['p_stitching_staff']; ?></div>
                            <div class="text-center font-bold <?php 
                                $statusCls = strtolower($itm['jobstatus']);
                                if(strpos($statusCls,'cut')!==false) echo 'bg-red-800 text-white';
                                elseif(strpos($statusCls,'stit')!==false) echo 'bg-yellow-900 text-white';
                                elseif(strpos($statusCls,'ready')!==false) echo 'bg-green-800 text-white';
                                elseif(strpos($statusCls,'delivered')!==false) echo 'bg-blue-800 text-white';
                                else echo 'bg-gray-700 text-white';
                            ?> rounded"><?php echo $itm['jobstatus']; ?></div>
                        </div>
                    <?php endforeach; ?>
                </div>
            </div>
        <?php endforeach; ?>
    </div>

    <!-- Pagination -->
    <?php
    $totalPages = ceil($totalFiltered / $perPage);
    ?>
    <div class="flex justify-center mt-4 space-x-2 items-center">
        <span>Page <?php echo $page; ?> / <?php echo $totalPages; ?></span>

        <?php if($page > 1): ?>
            <a href="?page=<?php echo $page-1; ?>&searchKeyword=<?php echo urlencode($searchKeyword); ?>&filterKeyword=<?php echo urlencode($filterKeyword); ?>"
               class="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300">← Prev</a>
        <?php endif; ?>

        <?php if($page < $totalPages): ?>
            <a href="?page=<?php echo $page+1; ?>&searchKeyword=<?php echo urlencode($searchKeyword); ?>&filterKeyword=<?php echo urlencode($filterKeyword); ?>"
               class="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300">Next →</a>
        <?php endif; ?>
    </div>

<?php else: ?>
    <p class="text-center py-4 text-gray-600">No orders found</p>
<?php endif; ?>

</body>
</html>
