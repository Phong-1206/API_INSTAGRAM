import requests
import time
class Api:
  def __init__(self,cookie):
    self.cookie = cookie
    self.headers = {
  "accept":"*/*",
  "accept-encoding":"gzip",
  "accept-language":"vi",
  "content-length":"108",
  "content-type":"application/x-www-form-urlencoded",
  "cookie":self.cookie,
  "sec-ch-prefers-color-scheme":"light",
  "sec-ch-ua":'"Not:A-Brand";v="99", "Chromium";v="112"',
  "sec-ch-ua-full-version-list":'"Not:A-Brand";v="99.0.0.0", "Chromium";v="112.0.5615.137"',
  "sec-ch-ua-mobile":"?0",
  "sec-ch-ua-platform":'"Android"',
  "sec-ch-ua-platform-version":"",
  "sec-fetch-dest":"empty",
  "sec-fetch-mode":"cors",
  "sec-fetch-site":"same-origin",
  "user-agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
  "viewport-with":"980",
  "x-asbd-id":"129477",
#  "x-csrftoken":"tXXJ1kjEyqLBMYE7BAkK3GMGh5Sp4OlR",
  "x-csrftoken":self.cookie.split("csrftoken=")[1].split("; ")[0],
  "x-ig-app-id":"936619743392459",
  "x-ig-www-claim":"hmac.AR2zwMSN0Don48rlZLXiz42kYufC_mfBdAQBP4KfWBgGpCvP",
  "x-instagram-ajax":"1007753953",
  "x-requested-with":"XMLHttpRequest"}
    
  def Uid(self, username):
    data={"username":username}
    data_profile = {}
    reuid = requests.get(f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}",data=data, headers = self.headers)
    data_profile.update({"edge_followed_by":reuid.json()["data"]["user"]["edge_followed_by"]["count"],"edge_follow":reuid.json()["data"]["user"]["edge_follow"]["count"],"uid":reuid.json()["data"]["user"]["id"], "full_name":reuid.json()["data"]["user"]["full_name"]})
    #return reuid.split('"profile_id":"')[1].split('","')[0]
    return data_profile
    
  def IdPost(self, url_post):
    re_urlpost = requests.get(url_post).text
    return re_urlpost.split('media_id":"')[1].split('","')[0]
    
  def Follow(self, username):
    uid = self.Uid(username)["uid"]
    data={
      "container_module":"profile",
      "nav_chain":"PolarisProfileRoot:profilePage:1:via_cold_start",
      "user_id":uid
    }
    follow = requests.post(f"https://www.instagram.com/api/v1/friendships/create/{uid}/",data=data,headers=self.headers)
    status = follow.json()["status"]
    if "ok" in status:
      return True 
    return False
    
  def UnFollow(self, username):
    uid = self.Uid(username)["uid"]
    data={
      "container_module":"profile",
      "nav_chain":"PolarisProfileRoot:profilePage:1:via_cold_start",
      "user_id":uid
    }
    follow = requests.post(f"https://www.instagram.com/api/v1/friendships/destroy/{uid}/",data=data,headers=self.headers)
    status = follow.json()["status"]
    if "ok" in status:
      return True 
    return False
    
  def TymPost(self, url_post):
    id_post = self.IdPost(url_post)
    data = {
      "variables":"{'media_id':'"+id_post+"'}",
    }
    re_tympost = requests.post(f"https://www.instagram.com/api/v1/web/likes/{id_post}/like/",data=data , headers=self.headers)
    if '"status":"ok"' in re_tympost.text:
      return True
    return False 
    
  def UnTymPost(self, url_post):
    id_post = self.IdPost(url_post)
    data = {
      "variables":"{'media_id':'"+id_post+"'}",
    }
    re_tympost = requests.post(f"https://www.instagram.com/api/v1/web/likes/{id_post}/unlike/",data=data , headers=self.headers)
    if '"status":"ok"' in re_tympost.text:
      return True
    return False 
    
  def Comment(self, url_post, content):
    id_post = self.IdPost(url_post)
    data= {"comment_text":content}
    re_comment = requests.post(f"https://www.instagram.com/api/v1/web/comments/{id_post}/add/",data=data,headers=self.headers)
    if('"status":"ok"' in re_comment.text):
      return True
    return False
    
  def ListFriends_Follower(self, username):
    uid = self.Uid(username)["uid"]
    max_friends = self.Uid(username)["edge_follow"]
    re_fr = requests.get(f"https://www.instagram.com/api/v1/friendships/{uid}/following/?count=12", data={"count":"12"} , headers=self.headers)
    re_text = re_fr.json()
    if ('"status":"ok"' in re_fr.text and re_text["users"] == []):
      print("Tài khoản riêng Tư")
    elif ('"status":"ok"' in re_fr.text and re_text["users"] != []):
      list_friends = re_text['users']
      next_max_id = re_text['next_max_id']
      check_max_id = True
      while check_max_id == True:
        re_fr = requests.get(f"https://www.instagram.com/api/v1/friendships/{uid}/following/?count=12&max_id={next_max_id}", data={"count":"12","max_id":next_max_id} , headers=self.headers)
        re_fr_data = re_fr.json()
        list_friends_2 = re_fr_data['users']
        list_friends = list_friends+list_friends_2
        if re_fr.text.find('next_max_id') != -1:
          next_max_id = re_fr_data['next_max_id']
          check_max_id = True
        else:
          check_max_id = False
      for i in list_friends:
        print(f" {i['username']} | [{i['full_name']}]")
      len_list = len(list_friends)
      print(f"Đang theo dõi {len_list} người")
      return list_friends 
    else:
      return False
  
  def List_Friends_Fl_Me(self, username):
    uid = self.Uid(username)["uid"]
    max_friends = self.Uid(username)["edge_followed_by"]
    re_fr = requests.get(f"https://www.instagram.com/api/v1/friendships/{uid}/followers/?count=12&search_surface=follow_list_page", data={"count":"12","search_surface":"follow_list_page"} , headers=self.headers)
    re_text = re_fr.json()
    if ('"status":"ok"' in re_fr.text and re_text["users"] == []):
      print("Tài Khoản Riêng Tư")
    elif ('"status":"ok"' in re_fr.text and re_text["users"] != []):
      list_friends = re_text['users']
      if (re_fr.text.find("next_max_id")!=-1):
        next_max_id = re_text['next_max_id']
        check_max_id = True
        while check_max_id == True:
          data={"count":"12","max_id":next_max_id,"search_surface":"follow_list_page"}
          re_fr = requests.get(f"https://www.instagram.com/api/v1/friendships/{uid}/followers/?count=12&max_id={next_max_id}&search_surface=follow_list_page", data= data, headers=self.headers)
          re_fr_data = re_fr.json()
          list_friends_2 = re_fr_data['users']
          list_friends = list_friends+list_friends_2
          if re_fr.text.find('next_max_id') != -1:
            next_max_id = re_fr_data['next_max_id']
            print(next_max_id)
            check_max_id = True
          else:
            check_max_id = False
      for i in list_friends:
        print(f" {i['username']} | [{i['full_name']}]")
      return list_friends
    else:
      return False

  def UnFollow_ListFriend(self, username):
    list_friend = self.ListFriends_Follower(username)
    vl = 1
    if list_friend != False:
      for data_list in list_friend:
        uid = data_list["pk_id"]
        list_name = data_list["full_name"] 
        data={
      "container_module":"profile",
      "nav_chain":"PolarisProfileRoot:profilePage:1:via_cold_start",
      "user_id":uid
    }
        follow = requests.post(f"https://www.instagram.com/api/v1/friendships/destroy/{uid}/",data=data,headers=self.headers)
        if '"status":"ok"' in follow.text:
          print(f"{vl}. Đã hủy theo dõi {list_name} thành công")
        else: 
          print("Thất Bại Nha")
        vl+=1
    else:
      print("Die Cookie!! 5 Phút Sau Lấy Lại")

print(Api('# COOKIE INSTAGRAM').Follow("dev.ttp"))
