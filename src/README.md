# Scripts organization

This part contain assistent code for lots of important parts in the whole work process, listed as follows:

| File          | Description |
| :---          | ----------- |
| /nuXmv        | verification and post-process based on nuXmv tool.                     |
| /plcverif     | verification and post-process based on plcverif tool, combining nuXmv, cbmc and other ways.   |
| /simple_call_llm          | simply create a llm call based on OpenAI-compatiable api   |
| /langchain_create_agent   | create agent based on langchain chains.                    |
| /RAG_database             |           |
| /tools        | Package of all useful tools.|

# Toolchain Installation

This part should include necessary supportive tools for plc command-line compilation and validation.

The following tools have been written to gitignore, and you can manually install and run tools following the instruction

## A. Compilation toolchains
### 1. compilation tool matiec
```
git clone https://github.com/nucleron/matiec.git
cd matiec
apt-get install autoconf, flex, bison
apt-get install build-essential -y
autoreconf -i
./configure
make

# then append to system path
export MATIEC_INCLUDE_PATH= $path_to_LLM4PLC/matiec/lib
export MATIEC_C_INCLUDE_PATH= $path_to_LLM4PLC/matiec/lib/C
export PATH= $path_to_LLM4PLC/matiec:$PATH
# example use, detail command should see --help
# ./iec2iec or ./iec2c
```


### 2. install rusty
```
sudo apt-get install build-essential llvm-14-dev liblld-14-dev libz-dev lld libclang-common-14-dev
apt-get install                \
    build-essential             \
    llvm-14-dev liblld-14-dev   \
    libz-dev                    \
    lld                         \
    libclang-common-14-dev      \
    libpolly-14-dev            


# install rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
<!-- sudo apt-get install cargo -->
<!-- sudo apt install binutils -->

git clone https://github.com/PLC-lang/rusty.git --depth 1

cd rusty

cargo build

# export debug/plc to path
export PATH="$PATH:/path/to/rusty/target/debug"

# finally compiler ready

plc /path/to/your/file.st

```

## B. Validation toolchains
Validation tools are tools for generated code's formal verification to find potential bugs and 
validate the functional correctness of st code. toolchains as follows:

### 3. verification tool nuXmv
```
# You can handly get it if wget donnot work
wget https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.0.0-linux64.tar.gz
tar -xzvf nuXmv-2.0.0-linux64.tar.gz
# notice to append the bin to path (~/.bashrc)
export PATH=$PATH:/home/work/src/nuXmv-2.0.0-Linux/bin
```

### 4. cbmc
directly install it and no extra actions needed.
```
    apt-get install cbmc
```       

### 5. plcverif toolchains
plcverif translates PLC code and the specified requirements automatically to the input format 
of various model checker engines, and reports the result to the user in a convenient, 
easy-to-understand format.
plcverif commands to use:
```
    cd src
    mkdir plcverif
    cd plcverif
    wget https://plcverif-oss.gitlab.io/cern.plcverif.cli/releases/cern.plcverif.cli.cmdline.app.product-linux.gtk.x86_64.tar.gz
    tar -xvzf cern.plcverif.cli.cmdline.app.product-linux.gtk.x86_64.tar.gz         // direct unzip

    export PLCVERIF_PATH="/home/work/src/plcverif"
    export PATH="$PLCVERIF_PATH:$PATH"
```



