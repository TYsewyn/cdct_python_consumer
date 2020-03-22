#!/usr/bin/env bash

if [ "$(uname)" == "Darwin" ]; then
    echo "Mac OS X platform detected"
    if ! [ -x "$(command -v brew)" ]; then
		echo 'Brew is not installed, trying SDKMAN!'
		if ! [ -x "$(command -v sdk)" ]; then
			echo 'SDKMAN! is not installed, exiting.'
		else
			sdk install springboot
			spring --version
			spring install org.springframework.cloud:spring-cloud-cli:2.2.2.RELEASE
		fi
	else
		brew tap pivotal/tap
		brew install springboot
		spring --version
		spring install org.springframework.cloud:spring-cloud-cli:2.2.2.RELEASE
	fi
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo "GNU/Linux platform detected"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    echo "32 bits Windows NT platform detected"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    echo "64 bits Windows NT platform detected"
fi
