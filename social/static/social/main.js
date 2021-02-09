
var likeBtn = document.getElementsByClassName('like')
var unlikeBtn = document.getElementsByClassName('unlike')
var followBtn = document.getElementsByClassName('follow')
var unfollowBtn = document.getElementsByClassName('unfollow')
var postBtn = document.getElementsByClassName('post')

for (var i = 0; i < likeBtn.length; i++){
    likeBtn[i].addEventListener('click', function(e){
        e.preventDefault()
        var postId = this.dataset.post
        var action = this.dataset.action
        console.log('postId:', postId, 'action:', action)
        likePost(postId,action)
        
    })
}

for (var i = 0; i < unlikeBtn.length; i++){
    unlikeBtn[i].addEventListener('click', function(){
        var postId = this.dataset.post
        var action = this.dataset.action
        console.log('postId:', postId, 'action:', action)

        likePost(postId,action)
    })
}

for(var i = 0; i < followBtn.length; i++){
    followBtn[i].addEventListener('click', function(){
        var userId = this.dataset.profile
        var action = this.dataset.action
        console.log('userId:', userId, 'action:', action)

        followOrUnfollow(userId, action)
    })
}

for(var i = 0; i < unfollowBtn.length; i++){
    unfollowBtn[i].addEventListener('click', function(){
        var userId = this.dataset.profile
        var action = this.dataset.action
        console.log('userId:', userId, 'action:', action)

        followOrUnfollow(userId, action)
    })
}


function likePost(postId, action){
    var url = '/likepost/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body:JSON.stringify({'postId':postId, 'action': action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:', data)
        location.reload()
    })
}

function followOrUnfollow(userId, action){
    var url = '/follow_user/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body:JSON.stringify({'userId':userId, 'action':action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:', data)
        location.reload()
    })
}

var new_post = document.getElementById('post')
new_post.addEventListener('click', function(e){
    e.preventDefault()
    document.getElementById('post').classList.add('d-none')
    document.getElementById('form-post').classList.remove('d-none')
})
