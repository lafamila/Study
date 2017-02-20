# Image Style Transfer

Implementation of paper "Image Style Transfer Using Convolutional Neural Networks" [PAPER](http://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf)

"Image Style Transfer Using Convolutional Neural Networks" 논문의 구현코드입니다. [PAPER](http://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf)

## Getting Started

Image Style Transfer Only
Image Style Transfer 만 실행시킬 경우
```
run()
```

Image Style transfer & make the result gif format
Image Style transfer 실행 후 결과를 gif 형식으로 만들 경우
```
start(run())
```


### Requirements

Libraries
필요한 라이브러리입니다.


```
tensorflow
images2gif (optional for gif)
```

Model for CNN (trained by ImageNet VGG-19) [DOWNLOAD](http://www.vlfeat.org/matconvnet/models/imagenet-vgg-verydeep-19.mat)
학습된 CNN을 이용하기 위해 ImageNet VGG-19 모델파일이 필요합니다. [DOWNLOAD](http://www.vlfeat.org/matconvnet/models/imagenet-vgg-verydeep-19.mat)



### Installing

Edit <b>input & output image settings</b> and <b>Hyperparameter </b> in code.
code 내부의 image input output 경로와 hyperparameter 값을 변경합니다.

**TODO**
get image path & hyperparameter using parser (python option)


## Authors

* **Lee KyoungMin** - *Initial work* - [lafamila](https://github.com/lafamila/lafamila)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
