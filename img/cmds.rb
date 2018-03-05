API_KEY = "1557593aeb7012a6c6f839071dd30b9cf6443ce3"
if ARGV[0] == 'classify'
	puts `curl -X POST -F "dnp_positive_examples=@dnp_training.zip" -F "mqtt_positive_examples=@mqtt_training.zip" -F "http_positive_examples=@http_training.zip" -F "negative_examples=@random_training.zip" -F "name=packets" "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=1557593aeb7012a6c6f839071dd30b9cf6443ce3&version=2016-05-20"`
elsif ARGV[0] == 'test'
	puts `curl -X GET "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classifiers/#{ARGV[1]}?api_key=#{API_KEY}&version=2016-05-20"`
elsif ARGV[0] == 'train'
	puts `curl -X POST -F "guitars_positive_examples=@guitars.zip" -F "negative_examples=@cats.zip" -F "name=guitars" "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classifiers?api_key=1557593aeb7012a6c6f839071dd30b9cf6443ce3&version=2016-05-20"`
else
	puts 'No options'
end

#curl -X POST -F "guitars_positive_examples=@guitars.zip" -F "negative_examples=@cats.zip" -F "name=guitars" "https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classifiers?api_key=1557593aeb7012a6c6f839071dd30b9cf6443ce3&version=2016-05-20"
#{
#    "classifier_id": "guitars_2126270606",
#    "name": "guitars",
#    "status": "training",
#    "owner": "fa1c427a-37c8-4779-8d80-6b64570a32a8",
#    "created": "2018-01-23T00:30:30.206Z",
#    "classes": [
#        {
#            "class": "guitars"
#        }
#    ]
#}  
