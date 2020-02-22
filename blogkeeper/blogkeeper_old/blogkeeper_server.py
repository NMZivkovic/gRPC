import logging
import pyodbc
import grpc
from concurrent import futures

import blogkeeper_pb2_grpc
import blogkeeper_pb2

class BlogKeeperServer(blogkeeper_pb2_grpc.BlogKeeperServicer):
    def __init__(self):
       self.db = pyodbc.connect('Driver={SQL Server};'
                      'Server=NZIVKOVIC\SQLEXPRESS;'
                      'Database=BlogDB;'
                      'Trusted_Connection=yes;') 

    def GetInfo(self, request, context):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM [BlogDB].[dbo].[BlogSummary] where [Name] = \'{}\''.format(request.name))
        response = blogkeeper_pb2.BlogSummary()

        for data in cursor:
            response.name = data[1]
            response.number_of_articles = data[2]
            response.number_of_authors=data[3]

        return response


    def ListArticles(self, request, context):
        cursor = self.db.cursor()

        cursor.execute('SELECT * FROM [BlogDB].[dbo].[Article] WHERE BlogSummaryId IN (SELECT Id FROM BlogSummary WHERE Name = \'{}\')'.format(request.name))

        articles = []

        for data in cursor:
            article = blogkeeper_pb2.Article()
            article.title = data[1]
            article.author = data[2]
            article.category = data[3]
            articles.append(article)
            yield article

    def __del__(self):
        self.db.close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    blogkeeper_pb2_grpc.add_BlogKeeperServicer_to_server(BlogKeeperServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
