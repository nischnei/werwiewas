# Python Code for Backend and ML functions

## Installation

While you can also use pip for your dependencies, I recommend to use poetry:
```
curl -sSL https://install.python-poetry.org | python3 -
```

Some additional dependencies needed:
```
brew install ffmpeg
brew install llvm@15
```

Note that we need llvm at version 15 or lower as numba is not compatible with newer versions.
Therefore, for later install, we need to set the LLVM_CONFIG as follows:
```
export LLVM_CONFIG=/opt/homebrew/opt/llvm@15/bin/llvm-config
```

Finally, install all remaining dependencies. We just need to run the server and the server depends on all other packages used. So all dependencies are installed automatically from here.
```
cd python/backend
poetry env use python3.11
poetry install
```

## Run the server
After installing, the server can be run by simply calling:

```
poetry run server
```

## Run integration tests
So far only integration tests are implemented for the backend. You can run them with:
```
poetry run pytest
```