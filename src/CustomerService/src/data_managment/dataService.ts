import db from './db';

async function fetchDataFromDatabase(table: string): Promise<any[]> {
  try {
    const result = await db.query(`SELECT * FROM ${table}`);
    return result;
  } catch (error) {
    throw error;
  } finally {
    await db.end(); // Close the database connection after use
  }
}

interface WarehouseTableRow {
  id: number;
  efficiency: string;
  created_at: Date;
}

export async function fetchWarehouseData(): Promise<WarehouseTableRow[]> {
  const data = await db.query("SELECT * FROM warehouse");
  const rows: WarehouseTableRow[] = data.rows.map((row: any) => {
    return {
      id: row.id,
      efficiency: row.efficiency,
      created_at: row.created_at
    };
  });
  return rows;
}

interface LatencyTableRow {
  id: number;
  produced: Date;
  consumed: Date;
}

export async function fetchLatencyData(): Promise<LatencyTableRow[]> {
  const data = await db.query("SELECT * FROM latency");
  const rows: LatencyTableRow[] = data.rows.map((row: any) => {
    return {
      id: row.id,
      produced: row.produced,
      consumed: row.consumed
    };
  });
  return rows;
}

interface InventoryeTableRow {
  id: number;
  order_state: string;
  created_at: Date;
}

export async function fetchInventoryData(): Promise<InventoryeTableRow[]> {
  const data = await db.query("SELECT * FROM inventory");
  const rows: InventoryeTableRow[] = data.rows.map((row: any) => {
    return {
      id: row.id,
      order_state: row.order_state,
      created_at: row.created_at
    };
  });
  return rows;
}
