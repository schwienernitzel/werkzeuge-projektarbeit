> [!WARNING]
> These scripts are a work-in-progress and are not intended to work out of the box!

 **Apart from the instructions below, you may have to:**
- [ ] Adjust input & output paths
- [ ] Install additional libraries
- [ ] Adapt code

# 1. Set up Google API-Key
   ```bash
   export APIKEY=yourapikey
   ```
> Note: Replace `yourapikey` with your actual Google API key.

# 2. Install required packages
  ```bash
  sudo apt-get install python3 python3-pip
   ```
> Note: To set up the workspace, you have to install these required python packages.
   
# 3. Install required modules
  ```bash
  sudo pip3 install torch torchvision torchaudio tensorflow transformers bertopic HanTa langid google-api-python-client nltk matplotlib
   ```
> Note: To set up the workspace, you have to install these required python modules.