# Image Style Transfer

Implementation of paper "Image Style Transfer Using Convolutional Neural Networks" [PAPER](http://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf)

"Image Style Transfer Using Convolutional Neural Networks" 논문의 구현코드입니다. [PAPER](http://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf)

<img src="">

## Getting Started

Image Style Transfer Only<br>
Image Style Transfer 만 실행시킬 경우
```
run()
```

Image Style transfer & make the result gif format<br>
Image Style transfer 실행 후 결과를 gif 형식으로 만들 경우
```
start(run())
```


### Requirements

Environment - python 3.5 ( It can be on python 2.7 but be careful in calculation of integer and float type. )<br>
개발환경 - python 3.5 ( python 2.7 에서도 실행 가능하나 정수와 실수형 계산에 주의해야합니다. )
```
python 3.5
```

Libraries<br>
필요한 라이브러리입니다.


```
tensorflow
images2gif (optional for gif)
```

Model for CNN (trained by ImageNet VGG-19) [DOWNLOAD](http://www.vlfeat.org/matconvnet/models/imagenet-vgg-verydeep-19.mat)<br>
학습된 CNN을 이용하기 위해 ImageNet VGG-19 모델파일이 필요합니다. [DOWNLOAD](http://www.vlfeat.org/matconvnet/models/imagenet-vgg-verydeep-19.mat)<br>



### Installing

Edit <b>input & output image settings</b> and <b>Hyperparameter </b> in code.<br>
code 내부의 image input output 경로와 hyperparameter 값을 변경합니다.<br><br>

**TODO**<br>
get image path & hyperparameter using parser (python option)


## Authors

* **Lee KyoungMin** - *Initial work* - [lafamila](https://github.com/lafamila/lafamila)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
