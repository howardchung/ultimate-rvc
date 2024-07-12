# Ultimate RVC

An autonomous pipeline to create covers with any RVC v2 trained AI voice from YouTube videos or a local audio file. For developers who may want to add a singing functionality into their AI assistant/chatbot/vtuber, or for people who want to hear their favourite characters sing their favourite song.

Showcase: TBA

Setup Guide: TBA

![](images/webui_generate.png?raw=true)

Ultimate RVC is under constant development and testing, but you can try it out right now locally!

## Changelog

TBA

## Setup

### Install Git

Follow the instructions [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to install Git on your computer.

### Clone Ultimate RVC repository
Open a terminal and run the following commands to clone this entire repository and open it locally.
```
git clone https://github.com/JackismyShephard/ultimate-rvc
cd ultimate-rvc
```

### Install dependencies

#### Windows
Run the following command to install the necessary dependencies on Windows:
```
./urvc.bat install 
```
Note that this will install Visual Studio build tools in your Program Files directory and will install Miniconda in your user directory. 
The whole process may take upwards of 15 minutes, so grab a cup of coffee and wait.

#### Linux (Debian-based)

Run the following command to install the necessary dependencies on Debian-based Linux distributions (e.g. Ubuntu):
```
./urvc.sh install 
```
The command has been tested only on Ubuntu 22.04 and 24.04 so support for other distributions is not guaranteed. 
Also note that the command will install the CUDA 11.8 toolkit system-wide. In case you have problems, you may need to install the toolkit manually.

## Usage

#### PRO TIP: Use a GPU for faster processing

While it is possible to run the Ultimate RVC web app on a CPU, it is highly recommended to use a GPU for faster processing. On an NVIDIA 3080 GPU, the AI cover generation process takes approximately 1.5 minutes, while on a CPU, it takes approximately 15 minutes. No testing has been done on AMD GPUs, so no guarantees are made for their performance.

### Start the app




#### Windows

```
./urvc.bat run
```

#### Linux (Debian-based)

```
./urvc.sh run
```

Once the following output message `Running on local URL:  http://127.0.0.1:7860` appears, you can click on the link to open a tab with the web app.

### Manage models


#### Download models

![](images/webui_dl_model.png?raw=true)

Navigate to the `Download model` subtab under the `Manage models` tab, and paste the download link to an RVC model and give it a unique name.
You may search the [AI Hub Discord](https://discord.gg/aihub) where already trained voice models are available for download. You may refer to the examples for how the download link should look like.
The downloaded zip file should contain the .pth model file and an optional .index file.

Once the 2 input fields are filled in, simply click `Download`! Once the output message says `[NAME] Model successfully downloaded!`, you should be able to use it in the `Generate song covers` tab!

#### Upload models

![](images/webui_upload_model.png?raw=true)

For people who have trained RVC v2 models locally and would like to use them for AI cover generations.
Navigate to the `Upload model` subtab under the `Manage models` tab, and follow the instructions.
Once the output message says `[NAME] Model successfully uploaded!`, you should be able to use it in the `Generate song covers` tab!

#### Delete RVC models

TBA

### Generate song covers

#### One-click generation


![](images/webui_generate.png?raw=true)

- From the Voice model dropdown menu, select the voice model to use.
- In the song input field, copy and paste the link to any song on YouTube, the full path to a local audio file, or select a cached input song.
- Pitch should be set to either -12, 0, or 12 depending on the original vocals and the RVC AI modal. This ensures the voice is not *out of tune*.
- Other advanced options for vocal conversion, audio mixing and etc. can be viewed by clicking the  appropriate accordion arrow to expand.

Once all options are filled in, click `Generate` and the AI generated cover should appear in a less than a few minutes depending on your GPU.

#### Multi-step generation
TBA

## CLI
TBA

## Update to latest version

Run the following command to pull latest changes from the repository and reinstall dependencies. 
Note that the process may take upwards of 10 minutes.
#### Windows

```
./urvc.bat update
```

#### Linux (Debian-based)

```
./urvc.sh update
```

## Development mode

When developing new features or debugging, it is recommended to run the app in development mode. This enables hot reloading, which means that the app will automatically reload when changes are made to the code.

#### Windows

```
./urvc.bat dev
```

#### Linux (Debian-based)

```
./urvc.sh dev
```


## Terms of Use

The use of the converted voice for the following purposes is prohibited.

* Criticizing or attacking individuals.

* Advocating for or opposing specific political positions, religions, or ideologies.

* Publicly displaying strongly stimulating expressions without proper zoning.

* Selling of voice models and generated voice clips.

* Impersonation of the original owner of the voice with malicious intentions to harm/hurt others.

* Fraudulent purposes that lead to identity theft or fraudulent phone calls.

## Disclaimer

I am not liable for any direct, indirect, consequential, incidental, or special damages arising out of or in any way connected with the use/misuse or inability to use this software.
