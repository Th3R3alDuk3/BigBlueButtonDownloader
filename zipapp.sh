#!/bin/bash

if command -v "python3" &> /dev/null
then

  python3 -m pip install --requirement requirements.txt --upgrade --target "src"
  python3 -m zipapp src --main "main:main" --python "/usr/bin/env python3" --output "downloader.pyz" --compress

elif command -v "python" &> /dev/null
then

  version=$(python -c "import sys; print(sys.version_info.major)")

  if [ $version -eq 3 ]
  then

    python -m pip install --requirement requirements.txt --upgrade --target "src"
    python -m zipapp src --main "main:main" --python "/usr/bin/env python" --output "downloader.pyz" --compress

  else

    echo "reuqire python version >= 3"
    sleep 3

  fi

else

  echo "python not found"
  sleep 3

fi
