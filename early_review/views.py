import datetime

from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import (UserProductReviewAfterSpamSerializer, AuthUserSerializer, JsonFileUploadSerializer)
from .models import (UserProductReviewAfterSpam, AuthUser, JsonFileUpload,UserThreshold)
from rest_framework.decorators import detail_route, list_route, action

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import nltk
import pandas as pd

# nltk.download('movie_reviews')


class UserProductReviewAfterSpamViewSet(viewsets.ModelViewSet):
    queryset = UserProductReviewAfterSpam.objects.all()
    serializer_class = UserProductReviewAfterSpamSerializer

    # filter_fields = ['product_id']

    def list(self, request):
        self.queryset = self.queryset.filter_by_query_params(request)
        return super(UserProductReviewAfterSpamViewSet, self).list(request)

    @list_route()
    def early(self, request):
        product_id = request.GET.get('product_id', None)
        if not product_id:
            return Response(['Please Send product_id as query string.'])
        try:
            product_review = UserProductReviewAfterSpam.objects.filter(product_id=product_id)
            first_date = product_review.order_by('date_review').first().date_review
            last_date = product_review.order_by('date_review').last().date_review
            difference = (last_date - first_date) / 3
            second_date = first_date + datetime.timedelta(days=difference.days)
            output_data = UserProductReviewAfterSpam.objects.filter(date_review__gte=first_date,
                                                                    date_review__lte=second_date)
        except UserProductReviewAfterSpam.DoesNotExist:
            return Response(['Please send valid new product_id.'])
        early_rating_tot = 0
        lst_data = []
        for row in output_data:
            dct_data = {}
            dct_data['id'] = row.id
            dct_data['product_id'] = row.product_id
            dct_data['product_name'] = row.product_name
            dct_data['reviewer_id'] = row.reviewer_id
            dct_data['reviewer_name'] = row.reviewer_name
            dct_data['review_text'] = row.review_text
            dct_data['overall_rating'] = row.overall_rating
            early_rating_tot += row.overall_rating
            dct_data['summary_product'] = row.summary_product
            dct_data['timestamp_review'] = row.timestamp_review
            dct_data['date_review'] = row.date_review
            lst_data.append(dct_data)
        rating_avg = early_rating_tot/len(output_data)
        early_count = len(output_data)
        data = {'rating_avg':rating_avg,'early_count':early_count ,'data':lst_data}
        return Response(data)

    @list_route()
    def middle(self, request):
        product_id = request.GET.get('product_id', None)
        if not product_id:
            return Response(['Please Send product_id as query string.'])
        try:
            product_review = UserProductReviewAfterSpam.objects.filter(product_id=product_id)
            first_date = product_review.order_by('date_review').first().date_review
            last_date = product_review.order_by('date_review').last().date_review
            difference = (last_date - first_date) / 3
            second_date = first_date + datetime.timedelta(days=difference.days)
            third_date = second_date + datetime.timedelta(days=difference.days)
            print(second_date, third_date)
            output_data = UserProductReviewAfterSpam.objects.filter(date_review__gt=second_date,
                                                                    date_review__lte=third_date)
        except UserProductReviewAfterSpam.DoesNotExist:
            return Response(['Please send valid new product_id.'])
        middle_rating_tot = 0
        lst_data = []
        for row in output_data:
            dct_data = {}
            dct_data['id'] = row.id
            dct_data['product_id'] = row.product_id
            dct_data['product_name'] = row.product_name
            dct_data['reviewer_id'] = row.reviewer_id
            dct_data['reviewer_name'] = row.reviewer_name
            dct_data['review_text'] = row.review_text
            dct_data['overall_rating'] = row.overall_rating
            middle_rating_tot+=row.overall_rating
            dct_data['summary_product'] = row.summary_product
            dct_data['timestamp_review'] = row.timestamp_review
            dct_data['date_review'] = row.date_review
            lst_data.append(dct_data)
        rating_avg = middle_rating_tot / len(output_data)
        middle_count=len(output_data)
        data = {'rating_avg': rating_avg,'middle_count':middle_count, 'data': lst_data}

        return Response(data)

    @list_route()
    def laggard(self, request):
        product_id = request.GET.get('product_id', None)
        if not product_id:
            return Response(['Please Send product_id as query string.'])
        try:
            product_review = UserProductReviewAfterSpam.objects.filter(product_id=product_id)
            first_date = product_review.order_by('date_review').first().date_review
            last_date = product_review.order_by('date_review').last().date_review
            difference = (last_date - first_date) / 3
            second_date = first_date + datetime.timedelta(days=difference.days)
            third_date = second_date + datetime.timedelta(days=difference.days)
            fourth_date = third_date + datetime.timedelta(days=difference.days)
            print(third_date, fourth_date)
            output_data = UserProductReviewAfterSpam.objects.filter(date_review__gt=third_date,
                                                                    date_review__lte=fourth_date)
        except UserProductReviewAfterSpam.DoesNotExist:
            return Response(['Please send valid new product_id.'])
        laggard_rating_tot = 0
        lst_data = []
        for row in output_data:
            dct_data = {}
            dct_data['id'] = row.id
            dct_data['product_id'] = row.product_id
            dct_data['product_name'] = row.product_name
            dct_data['reviewer_id'] = row.reviewer_id
            dct_data['reviewer_name'] = row.reviewer_name
            dct_data['review_text'] = row.review_text
            dct_data['overall_rating'] = row.overall_rating
            laggard_rating_tot+=row.overall_rating
            dct_data['summary_product'] = row.summary_product
            dct_data['timestamp_review'] = row.timestamp_review
            dct_data['date_review'] = row.date_review
            lst_data.append(dct_data)
        rating_avg = laggard_rating_tot / len(output_data)
        laggard_count=len(output_data)
        data = {'rating_avg': rating_avg,'laggard_count':laggard_count, 'data': lst_data}

        return Response(data)

    @list_route()
    def sentimental_analysis(self, request):
        product_id = request.GET.get('product_id', None)
        if not product_id:
            return Response(['Please Send product_id as query string.'])
        try:
            product_review = UserProductReviewAfterSpam.objects.filter(product_id=product_id)
            first_date = product_review.order_by('date_review').first().date_review
            last_date = product_review.order_by('date_review').last().date_review
            difference = (last_date - first_date) / 3
            second_date = first_date + datetime.timedelta(days=difference.days)
            output_data = UserProductReviewAfterSpam.objects.filter(date_review__gte=first_date,
                                                                    date_review__lte=second_date)
        except UserProductReviewAfterSpam.DoesNotExist:
            return Response(['Please send valid new product_id.'])

        def extract_features(word_list):
            return dict([(word, True) for word in word_list])

        def sentimental_output(review_text):
            print("POSITIVE", review_text)
            print("MOVIE-REVIEWS", movie_reviews.fileids('pos')[0][0])
            # print("PPPPATH",os.path(movie_reviews.fileids('pos')[0]))
            positive_fileids = movie_reviews.fileids('pos')
            # print("POSITIVE>>>", positive_fileids)
            negative_fileids = movie_reviews.fileids('neg')
            # print("negative>>>", negative_fileids)
            features_positive = [(extract_features(movie_reviews.words(fileids=[f])), 'Positive') for f in
                                 positive_fileids]
            features_negative = [(extract_features(movie_reviews.words(fileids=[f])), 'Negative') for f in
                                 negative_fileids]
            threshold_factor = 0.8
            threshold_positive = int(threshold_factor * len(features_positive))
            threshold_negative = int(threshold_factor * len(features_negative))
            features_train = features_positive[:threshold_positive] + features_negative[:threshold_negative]
            features_test = features_positive[threshold_positive:] + features_negative[threshold_negative:]
            # print("\nNumber of training datapoints:", len(features_train))
            # print("Number of test datapoints:", len(features_test))

            classifier = NaiveBayesClassifier.train(features_train)
            print("\nAccuracy of the classifier:", nltk.classify.util.accuracy(classifier, features_test))

            # print("\nTop 10 most informative words:")
            # for item in classifier.most_informative_features()[:10]:
            #     print(item[0])

            print("\nPredictions:")

            print("\nReview:", review_text)
            probdist = classifier.prob_classify(extract_features(review_text.split()))
            pred_sentiment = probdist.max()

            print("Predicted sentiment:", pred_sentiment)
            print("Probability:", round(probdist.prob(pred_sentiment), 2))
            lst_data = []
            dct_data = {}
            dct_data['product_name'] = row.product_name
            dct_data['reviewer_name'] = row.reviewer_name
            dct_data['review_text'] = review_text
            dct_data['predicted_sentiment'] = pred_sentiment
            dct_data['Probability'] = round(probdist.prob(pred_sentiment), 2)
            lst_data.append(dct_data)
            return lst_data

        lst = []
        for row in output_data:
            lst.extend(sentimental_output(row.review_text))

        return Response(lst)


class AuthUserViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    def login(self, request):

        email_str = request.data.get('email', None)
        password_str = request.data.get('password', None)

        email = email_str.strip()
        password = password_str.strip()

        if email and password:

            user = authenticate(email=email, password=password)
            if not user:
                return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                token = Token.objects.get_or_create(user=user)
                return Response({'token': str(token[0]), 'message': 'login successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'provide email and password'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def register(self, request):

        email_str = request.data.get('email', None)
        password_str = request.data.get('password', None)
        user_name_str = request.data.get('username', None)

        email = email_str.strip()
        password = password_str.strip()
        user_name = user_name_str.strip()

        if email and password and user_name:
            try:
                user = AuthUser.objects.get_by_natural_key(email)
                return Response({'error': 'user already exist'}, status=status.HTTP_400_BAD_REQUEST)

            except AuthUser.DoesNotExist:
                app_user = AuthUser.objects.create_user(email, password, user_name)
                token = Token.objects.get_or_create(user=app_user)
                return Response({'token': str(token[0]),'message': 'registered successfully'}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'provide email and password'}, status=status.HTTP_400_BAD_REQUEST)


class AuthUserModelViewSet(viewsets.ModelViewSet):
    queryset = AuthUser.objects.all()
    serializer_class = AuthUserSerializer

    def list(self, request):
        query_str = request.GET.get('query', None)

        if query_str:
            self.queryset = self.queryset.filter(username__icontains=query_str.strip())
        return super(AuthUserModelViewSet, self).list(request)


class FileUploadViewSet(viewsets.ModelViewSet):
    serializer_class = JsonFileUploadSerializer
    queryset = JsonFileUpload.objects.all()

    # def list(self, request):
    #     return Response("list")
    @transaction.atomic
    def create(self, request):
        try:
            df = pd.read_json(request.data['file_upload'], lines=True)
            lst = []
            for row, value in df.iterrows():
                user_id = value.reviewerID
                user_name = value.reviewerName
                review = value.reviewText

                # product_id = request.GET.get('product_id', None)
                # if not product_id:
                #     return Response(['Please Send product_id as query string.'])
                # try:
                #     product_review = UserProductReviewAfterSpam.objects.filter(product_id=product_id)
                #     first_date = product_review.order_by('date_review').first().date_review
                #     last_date = product_review.order_by('date_review').last().date_review
                #     difference = (last_date - first_date) / 3
                #     second_date = first_date + datetime.timedelta(days=difference.days)
                #     output_data = UserProductReviewAfterSpam.objects.filter(date_review__gte=first_date,
                #                                                             date_review__lte=second_date)
                # except UserProductReviewAfterSpam.DoesNotExist:
                #     return Response(['Please send valid new product_id.'])

                def extract_features(word_list):
                    return dict([(word, True) for word in word_list])

                def sentimental_output(review_text):
                    positive_fileids = movie_reviews.fileids('pos')
                    negative_fileids = movie_reviews.fileids('neg')
                    # for f in positive_fileids:
                    #     # print(">>>>>", f)
                    #     print(extract_features(movie_reviews.words(fileids=[f])))

                    features_positive = [(extract_features(movie_reviews.words(fileids=[f])), 'Positive')
                                         for f in positive_fileids]
                    # print("POSITIVE", features_positive)
                    features_negative = [(extract_features(movie_reviews.words(fileids=[f])), 'Negative')
                                         for f in negative_fileids]
                    threshold_factor = 0.8
                    # print("lelen", features_positive)
                    threshold_positive = int(threshold_factor * len(features_positive))
                    threshold_negative = int(threshold_factor * len(features_negative))
                    features_train = features_positive[:threshold_positive] + features_negative[:threshold_negative]
                    features_test = features_positive[threshold_positive:] + features_negative[threshold_negative:]

                    classifier = NaiveBayesClassifier.train(features_train)
                    # print("CLASSIDFOE", list(classifier))

                    # for f in review_text.split():
                    #     print("SPLIT", classifier.prob_classify(extract_features(f)))
                    probdist = classifier.prob_classify(extract_features(review_text.split()))
                    # print("IIII", probdist)
                    pred_sentiment = probdist.max()
                    # print("MAX", pred_sentiment)

                    user = UserThreshold.objects.filter(reviewer_id=user_id)
                    print("SSSS", user)
                    if not user:
                        # print("hello")
                        if pred_sentiment == "Positive":
                            print("hello3")
                            user = UserThreshold.objects.create(reviewer_id=user_id, reviewer_name=user_name, sentiment_threshold=1)
                            print("hello4")
                            user.save()
                            print("hello5")
                        else:
                            user = UserThreshold.objects.create(reviewer_id=user_id, reviewer_name=user_name, sentiment_threshold=0)
                            user.save()
                    else:
                        print("elseeeeeeeee")
                        sentimental = UserThreshold.objects.filter(reviewer_id=user_id).last()
                        print("hello1",sentimental)
                        if pred_sentiment == "Positive":
                            print("elseeeeeeeee1")
                            avg = (sentimental.sentiment_threshold + 1)/2
                            sentimental.sentiment_threshold = avg
                            print("SAVE")
                            sentimental.save()
                        else:
                            print("elseeeeeeeee2")
                            avg = sentimental.sentiment_threshold / 2
                            sentimental.sentiment_threshold = avg
                            print("B$ SAVE")
                            sentimental.save()



                    # lst_data = []
                    # dct_data = {}
                    # dct_data['reviewer_id'] = user_id
                    # dct_data['reviewer_name'] = user_name
                    # dct_data['review_text'] = review_text
                    # dct_data['Predicted Sentiment'] = pred_sentiment
                    # dct_data['Probability'] = round(probdist.prob(pred_sentiment), 2)
                    # lst_data.append(dct_data)


                    # return lst_data
                    # return ("success")


                # lst.extend(sentimental_output(review))
                sentimental_output(review)
            print("hello66")
            return Response("success")





            # df.columns = list(map(lambda x: x.strip().replace(' ', '_'), df.columns))
            # df['waiver'] = df['waiver'].astype(float)
            # df['waiver'] = df['waiver'].fillna(0)
            # df = df.fillna('')
            # df[['container_number', 'lease_yard']] = df[['container_number', 'lease_yard']].astype(str)
            # df['off_hire_date'] = pd.to_datetime(df['off_hire_date'])
            # df[['container_number', 'lease_yard']] = df[['container_number', 'lease_yard']].apply(
            #     lambda x: x.str.strip().str.upper())
            # lst_data = []
            # for row, value in df.iterrows():
            #     dct_data = {}
            #     try:
            #         container = Container.objects.get(number__iexact=value.container_number)
            #     except:
            #         continue
            #     dct_data['container_number_id'] = container.id
            #     dct_data['container_number'] = container.number
            #     dct_data['container_type_id'] = container.container_type.id
            #     dct_data['container_type'] = container.container_type.name
            #     dct_data['line_id'] = container.line.id if container.line else None
            #     dct_data['line'] = container.line.code if container.line else ''
            #     dct_data['location_id'] = container.move_history.last().location.id if container.move_history else None
            #     dct_data['location'] = container.move_history.last().location.code if container.move_history else ''
            #     dct_data['off_hire_date'] = value.off_hire_date
            #     try:
            #         yard = Yard.objects.get(code__iexact=value.lease_yard)
            #     except:
            #         continue
            #     dct_data['yard_id'] = yard.pk
            #     dct_data['yard'] = value.lease_yard
            #     dct_data['waiver'] = value.waiver
            #     lst_data.append(dct_data)
        except:
            return Response(['Please upload proper file'])
        else:
            return Response("success")
