import logging
import grpc

import blogkeeper_pb2
import blogkeeper_pb2_grpc

class BlogKeeperClient():
    def __init__(self, ip_port):
        channel = grpc.insecure_channel(ip_port)
        self.stub = blogkeeper_pb2_grpc.BlogKeeperStub(channel)

    def get_blog_summary(self, blog_name):
        blog = blogkeeper_pb2.Blog(name=blog_name)
        return self.stub.GetInfo(blog)

    def get_list_of_articles(self, blog_name):
        blog = blogkeeper_pb2.Blog(name=blog_name)
        return self.stub.ListArticles(blog)


def run():

    client = BlogKeeperClient('localhost:50051')

    info = client.get_blog_summary('RubiksCode')
    print('--------Blog Summary--------')
    print(info)
    print('----------------------------')

    articles = client.get_list_of_articles('RubiksCode')
    print('--------Articles-------')
    for article in articles:
        print(article)
        print('----------------------')


if __name__ == '__main__':
    logging.basicConfig()
    run()