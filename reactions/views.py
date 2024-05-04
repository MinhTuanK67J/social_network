from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone

from .models import Reactions
from .serializers import ReactionsSerializer

from posts.models import Posts
from comments.models import Comments

from common_functions.common_function import getUser

from notifications.views import createReactNotification

from userprofiles.views import UserProfileBasicView

# Create your views here.
class GetReactions(APIView):
    def post(self, request):
        user = getUser(request)
        
        if user is None:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # print(request.data)
        
        posts_id = int(request.data.get('posts_id'))
        comment_id = int(request.data.get('comment_id'))
        
        topMostReacted = None
        total = None
        
        if comment_id < 0:
            post = Posts.objects(__raw__={'_id': posts_id}).first()
            if post is None:
                return Response({'error': 'Posts not found'}, status=status.HTTP_404_NOT_FOUND)
            topMostReacted = post.getMostUseReactions()
            total = post.number_of_reactions.total
        elif comment_id > 0:
            comment = Comments.objects(__raw__={'_id': comment_id}).first()
            if comment is None:
                return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
            topMostReacted = comment.getMostUseReactions()
            total = comment.number_of_reactions.total
            
        response = Response()
        response.data = {
            'total': total,
            'topMostReacted': topMostReacted,
        }
        return response

class CreateReaction(APIView):
    def createReaction(self, request, user):
        return Reactions(user=UserProfileBasicView().getUserProfileBasic(user), 
                         to_posts_id=request.data.get('posts_id'), 
                         to_comment_id=request.data.get('comment_id'), 
                         type=request.data.get('type'),
                         created_at=timezone.now(), 
                         updated_at=timezone.now())
    
    def changeTypeReactionIfIsReacted(self, request, user_id, posts_id, comment_id):
        checkIsReacted = IsReactedView().checkIsReacted(user_id, posts_id, comment_id)
        
        if checkIsReacted.get('is_reacted'):
            reaction = checkIsReacted.get('reaction')
            currentType = reaction.type
            newType = request.data.get('type')
            
            print(currentType, newType)
            
            if currentType == newType:
                return True
            
            # change type reaction to new type
            reaction.setTypeReaction(newType)
            reaction.save()
            
            # change number of type reactions
            is_for_posts = comment_id < 0
            if is_for_posts:
                post = Posts.objects(__raw__={'_id': posts_id}).first()
                if post is None:
                    return False
                post.changeTypeReaction(currentType, newType)
                post.save()
            elif is_for_posts == False:
                comment = Comments.objects(__raw__={'_id': comment_id}).first()
                if comment is None:
                    return False
                comment.changeTypeReaction(currentType, newType)
                comment.save()
            
            createReactNotification(reaction)
            
            return True
            
        return False
    
    def post(self, request):
        user = getUser(request)
        
        if user is None:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.data.get('type') not in ['like', 'love', 'haha', 'wow', 'sad', 'angry', 'care']:
            return Response({'error': 'Invalid type'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('posts_id') is None and request.data.get('comment_id') is None:
            return Response({'error': 'posts_id or comment_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('user_id') is None or request.data.get('user_name') is None or request.data.get('user_avatar') is None:
            return Response({'error': 'user_id, user_name, user_avatar is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if int(request.data.get('user_id')) != user.id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response()
        
        posts_id = int(request.data.get('posts_id'))
        comment_id = int(request.data.get('comment_id'))
        
        if self.changeTypeReactionIfIsReacted(request, user.id, posts_id, comment_id):
            return Response({'success': 'Type reaction is changed'})
        
        try:
            reaction = self.createReaction(request, user)
            reaction.save()
            
            if comment_id < 0:
                post = Posts.objects(__raw__={'_id': posts_id}).first()
                if post is None:
                    reaction.delete()
                    return Response({'error': 'Posts not found'}, status=status.HTTP_404_NOT_FOUND)
                post.inc_reaction(reaction.type)
                post.save()
            elif comment_id > 0:
                comment = Comments.objects(__raw__={'_id': comment_id}).first()
                if comment is None:
                    reaction.delete()
                    return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
                comment.inc_reaction(reaction.type)
                comment.save()
                
            createReactNotification(reaction)
                
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = ReactionsSerializer(reaction)
        
        response.data = {
            'reaction': serializer.data
        }
        return response

class DeleteReaction(APIView):
    def post(self, request):
        user = getUser(request)
        
        if user is None:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response()
        
        user_id = user.id
        posts_id = int(request.data.get('posts_id'))
        comment_id = int(request.data.get('comment_id'))

        try:
            reaction = Reactions.objects(__raw__={'to_posts_id': posts_id, 
                                                  'to_comment_id': comment_id, 
                                                  'user.id': user_id}).first()
            
            if reaction is None:
                return Response({'error': 'Reaction not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if comment_id < 0:
                post = Posts.objects(__raw__={'_id': posts_id}).first()
                if post is None:
                    return Response({'error': 'Posts not found'}, status=status.HTTP_404_NOT_FOUND)
                post.dec_reaction(reaction.type)
                post.save()
            elif comment_id > 0:
                comment = Comments.objects(__raw__={'_id': comment_id}).first()
                if comment is None:
                    return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
                comment.dec_reaction(reaction.type)
                comment.save()
                
            reaction.delete()
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        response.data = {
            'message': 'Reaction removed'
        }
        return response

class IsReactedView(APIView):
    def checkIsReacted(self, user_id, posts_id, comment_id):
        reaction = Reactions.objects(__raw__={  'to_posts_id': posts_id, 
                                                'to_comment_id': comment_id,
                                                'user.id': user_id}).first()
        
        is_reacted = (reaction != None)
        result = {
            'is_reacted': is_reacted
        }
        
        if is_reacted:
            result['type'] = reaction.type
            result['reaction'] = reaction
        
        return result
    
    def post(self, request):
        user = getUser(request)
        
        if user is None:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response()
        
        user_id = user.id
        posts_id = int(request.data.get('posts_id'))
        comment_id = int(request.data.get('comment_id'))
        
        ret = self.checkIsReacted(user_id, posts_id, comment_id)
        response.data = {
            'is_reacted': ret.get('is_reacted'),
            'type' : ret.get('type') or ''
        }
            
        return response