#!/bin/bash -e

if [ -n "${DEBUG}" ] ; then
    BUILD_TYPE=Debug
else
    BUILD_TYPE=Release
fi

if [ -z "${PLATFORM}" ]; then
    SYSNAME="$(uname -s)"
fi

case "${SYSNAME}" in
    Darwin)
        export PLATFORM="mac"
        LOCAL_LIBRARY="${PLATFORM}/libcryptosdk.dylib"

        PYTHON_VERSION=`python -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";`
        PYTHON_LIBRARY=/usr/local/Frameworks/Python.framework/Versions/${PYTHON_VERSION}/lib/libpython${PYTHON_VERSION}.dylib
        PYTHON_INCLUDE_DIR=/usr/local/Frameworks/Python.framework/Versions/${PYTHON_VERSION}/Headers/

        CMAKE_ADDITIONAL_ARGS=-DPYTHON_LIBRARY="${PYTHON_LIBRARY} -DPYTHON_INCLUDE_DIR=${PYTHON_INCLUDE_DIR}"

        ;;
    Linux)
        export PLATFORM="linux"
        LOCAL_LIBRARY="${PLATFORM}/libcryptosdk.so"

        ;;
    *)
        echo "Unsupported system ${SYSNAME}!"
        exit 1

        ;;
esac

echo "Building ${BUILD_TYPE} version for ${PLATFORM:-$(uname -s)}..."

# Copy external crypto-sdk dependencies.
CRYPTO_SDK_BUILD_DIR=native

mkdir -p build/${PLATFORM}
cp -f ${CRYPTO_SDK_BUILD_DIR}/${LOCAL_LIBRARY} build/${PLATFORM}/

pushd build

(cd ../ && CMAKE_ONLY=1 ./clean.sh)
cmake .. ${CMAKE_ADDITIONAL_ARGS} -DCMAKE_BUILD_TYPE=${BUILD_TYPE} -DPLATFORM=${PLATFORM}
make

popd

cp -f build/${PLATFORM}/lib/pycrypto.so orbs_client/
cp -f native/${LOCAL_LIBRARY} build/orbs_client

mkdir -p build/lib/orbs_client
cp -f build/${PLATFORM}/lib/pycrypto.so build/lib/orbs_client
cp -f native/${LOCAL_LIBRARY} build/lib/orbs_client

rm -rf build/lib/CMakeFiles

# cp -f build/${PLATFORM}/lib/pycrypto.so test/

./test.sh
