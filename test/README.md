# Zombie Factory Smart Contract

## Description

This Solidity smart contract provides a basic implementation for creating and managing zombies. It allows users to generate zombies with unique DNA based on their name.  This is a foundational contract and can be extended with additional functionality for a more complex zombie-themed game or application.

## Installation

1.  **Prerequisites:**  Ensure you have a Solidity development environment set up.  This typically includes:
    *   Node.js and npm (Node Package Manager)
    *   Truffle or Hardhat (development frameworks)
    *   Ganache (local blockchain emulator) or access to a test network (e.g., Ropsten, Rinkeby).
    *   Solidity compiler (solc)

2.  **Project Setup:**
    *   Create a new project directory.
    *   Initialize your project using Truffle: `truffle init` or Hardhat: `npx hardhat`.
    *   Copy the `zombie_game.sol` contract file into your project's `contracts` directory.

3.  **Compilation:**
    *   Compile the contract using Truffle: `truffle compile` or Hardhat: `npx hardhat compile`.

4.  **Deployment:**
    *   Configure your Truffle or Hardhat configuration file (`truffle-config.js` or `hardhat.config.js`) to connect to your desired Ethereum network (Ganache or a testnet).
    *   Create a deployment script in your `migrations` directory (for Truffle) or `scripts` directory (for Hardhat) to deploy the contract.
    *   Deploy the contract using Truffle: `truffle migrate` or Hardhat: `npx hardhat run scripts/deploy.js --network <network_name>`.  Replace `<network_name>` with the name of your configured network (e.g., `development`, `ropsten`).

## Usage Examples

After deploying the contract, you can interact with it using tools like Truffle Console, Hardhat Console, or web3.js.

1.  **Creating a Random Zombie:**

    ```javascript
    // Example using web3.js (after deploying the contract and obtaining the contract address)
    const contract = new web3.eth.Contract(abi, contractAddress); // Replace abi and contractAddress

    contract.methods.createRandomZombie("Alice").send({ from: account })
    .then(result => {
        console.log("Zombie created:", result);
    });

    // You'll need to replace 'abi', 'contractAddress', and 'account' with your actual values.
    ```

2.  **Accessing Zombie Information:**

    ```javascript
    // Example using web3.js
    contract.methods.zombies(0).call()
    .then(zombie => {
        console.log("Zombie Name:", zombie.name);
        console.log("Zombie DNA:", zombie.dna);
    });
    ```

## Features Overview

*   **Zombie Creation:** Allows users to create new zombies with randomly generated DNA.
*   **DNA Generation:** Generates unique DNA for each zombie based on its name using `keccak256` hashing.
*   **Zombie Storage:** Stores created zombies in an array within the contract.
*   **Basic Structure:** Provides a fundamental structure for building a more advanced zombie-based application.

## File Structure Summary

*   `contracts/zombie_game.sol`: Contains the Solidity source code for the `ZombieFactory` contract.
*   `migrations/`: (Truffle) Contains deployment scripts.
*   `scripts/`: (Hardhat) Contains deployment scripts and other utility scripts.
*   `truffle-config.js`: (Truffle) Configuration file for Truffle.
*   `hardhat.config.js`: (Hardhat) Configuration file for Hardhat.

## Important Notes

*   **Gas Costs:** Creating zombies and interacting with the contract will incur gas costs.
*   **Randomness:** The `_generateRandomDna` function uses `keccak256` which while reasonably unpredictable, is still deterministic based on the input.  For production applications requiring stronger randomness, consider using Chainlink VRF or similar oracle services.
*   **Error Handling:**  This contract lacks explicit error handling. Implement appropriate error handling mechanisms (e.g., `require` statements) for robust production deployments.
*   **Security:**  This contract is a basic example and might be vulnerable to security exploits. Thoroughly audit your code before deploying to a production environment. Consider common attack vectors such as integer overflows/underflows and reentrancy attacks.
*   **Future Development:** This contract can be extended with features such as zombie breeding, combat mechanics, and ownership management.
