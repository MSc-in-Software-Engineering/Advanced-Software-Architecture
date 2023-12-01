import { fetchInventoryData, fetchLatencyData, fetchWarehouseData } from "./data_managment/dataService";

const figlet = require("figlet");
const promptly = require("promptly");

console.log(figlet.textSync("Customer Service CLI"));
console.info("Welcome to the Customer Service CLI")

async function startCLI() {
    while (true) {
        try {
            console.info("What do you want to do?")
            var choice = await promptly.choose("Enter your choice [d - See supply chain data, r - Request Products, q - Quit]: ", ["d", "r", "q"]);

            if (choice === "d") {
                await supplyChainData();
            } else if (choice === "r") {
                const amount = await promptly.prompt("Enter the number of products to request: ", { validator: Number });
                console.info(`Requesting ${amount} products`);
            } else if (choice === "q") {
                console.log("Quitting the Customer Service CLI. Goodbye!");
                break;
            }
            console.info("");
        } catch (error) {
            console.error("Error occurred:", error);
        }
    }
}

async function supplyChainData() {
    console.info("What kind of data are you looking for?");
    const choice = await promptly.choose("Enter your choice [w - Warehouse data, l - Latency data, i - Inventory data, n - None]: ", ["w", "l", "i", "n"]);
    if (choice === "w") {
        console.info("Displaying Warehouse data");
        const data = await fetchWarehouseData();
        console.table(data);
    } else if (choice === "l") {
        console.info("Displaying Latency data");
        const data = await fetchLatencyData();
        console.table(data);
    } else if (choice === "i") {
        console.info("Displaying Inventory data");
        const data = await fetchInventoryData();
        console.table(data);
    }
}


function listCurInventory() {
    try {
        console.info("Current amount of products in inventory: 0");
    } catch (error) {
        console.error("Error occured while reading the inventory!", error);
    }
}

function requestProducts(amount: Number) {
    try {
        console.info("Requesting " + amount + " products");
    } catch (error) {
        console.error("Error occured while requesting products!", error);
    }
}

startCLI()