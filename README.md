# CredentialSystem
# Bitcoin Core
1. Download and install Bitcoin Core --> bitcoin-0.19.0.1-win64-setup.exe
2. Set Up a Bitcoin Regtest Environment
   - Run bitcoin core --> C:\Bitcoin\bitcoin-qt.exe
   - Click on Settings -> Options -> Open Configuration File , after that Close bitcoin-qt
   - Add the following line to the configuration file, and then save:
     ```
      regtest=1
     ```    
3. Start Bitcoin
   - Open cmd and change to the directory --> C:\Bitcoin\daemon
   - Then run: 
     ```
      bitcoind
     ```
4. Create issuing address
   - Open second cmd and change to directory --> C:\Bitcoin\daemon, Run:
     ```
      bitcoin-cli getnewaddress "address_name"
     ```
5. Generate bitcoin to new address
   ```
    bitcoin-cli generatetoaddress 101 "address" 
   ```
# Install python
  ```
    python-3.8.1-amd64.exe 
  ```
# Issuing trust statement 
  Run: 
  ```
    issueTrust.py
  ```
# Issuing Credential
  Run: 
  ```
    issueCred.py
  ```
# Selective Disclosure
  Run: 
  ```
    showCred.py
  ```
# Verifying Credential
  Run: 
  ```
    verify.py
  ```
