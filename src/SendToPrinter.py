class SendToPrinter:

    def __init__(self, host, printer_name, api_key, post, MultipartEncoder, path):
        self.printer_name = printer_name
        self.host = host
        self.api_key = api_key
        self.post = post
        self.MultipartEncoder = MultipartEncoder
        self.path = path

    def upload(self, path_to_file):
        url = "http://{}:3344/printer/model/{}?a=upload".format(self.host, self.printer_name)
        
        file = open(path_to_file,'rb')
        filename = self.path.basename(file.name)

        m = self.MultipartEncoder(
            fields={'file': (filename, file, 'text/plain')}
        )

        headers = {
            'Content-Type' : m.content_type,
            'x-api-key' : self.api_key,
        }
        
        response = self.post(url=url, data=m, headers=headers)
        
        json_response = response.json()
        model_id = json_response['data'][-1]['id']
        print("uploaded gcode to printer: model id is {}".format(model_id))
        return model_id
