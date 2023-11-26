import http.server
import socketserver
import sqlite3
import json
import datetime
import ast
from urllib.parse import urlparse, parse_qs, unquote


#Création d'un handleur
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    
    # répertoire des documents statiques
    static_dir = '/client'
    
    #analyse de l'URL
    def parametres(self):
      # analyse de l'adresse
      infos = urlparse(self.path)
      self.path_infos = [unquote(v) for v in infos.path.split('/')[1:]]
      self.query_string = infos.query
      self.params = parse_qs(infos.query)

      # récupération du corps
      length = self.headers.get('Content-Length')
      ctype = self.headers.get('Content-Type')
      if length:
         self.body = str(self.rfile.read(int(length)),'utf-8')
         if ctype == 'application/x-www-form-urlencoded' :
           self.params = parse_qs(self.body)
      else:
         self.body = ''

      print(infos)
      print(self.path_infos)
      
    #gestion d'une erreur
    def send_static(self):
        self.path = self.static_dir + self.path
        
        #choix de la fonction à utiliser en foncftion des infos rentrées dans l'URL
        if (self.command=='HEAD'):
            http.server.SimpleHTTPRequestHandler.do_HEAD(self)
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)
            
        #self.send_error(404,"La page {} n'existe pas".format(self.path))
    
    #on surcharge la méthode HEAD                   
    def do_HEAD(self):
        self.send_static()
    
    def do_GET(self):
        # on récupère les paramètres
        self.parametres()
        print(self.path_infos)
        
        if self.path.startswith('/time'):
          self.send_time()
        
        # le chemin d'accès commence par le nom de projet au pluriel
        elif len(self.path_infos) > 0 and self.path_infos[0] == "ponts":
            self.send_json_ponts()

        # le chemin d'accès commence par le nom du projet au singulier, suivi par un nom de lieu
        elif len(self.path_infos) > 1 and self.path_infos[0] == "pont":
            self.send_json_pont(self.path_infos[1])
         
        
        elif len(self.path_infos) > 0 and self.path_infos[0] == "commentaires":
            self.get_commentaire()
            
        else:
            self.send_static()
  
    
  
    
# """ Fonctions pour la gestion des commentaires et des utilisateurs

    def do_POST(self):
      self.parametres()
      print("Post")
        #choix de la fonction à utiliser (si on ajoute un utilisateur ou un commentaire)
      if len(self.path_infos) > 0 and self.path_infos[0] == "commentaire":
        self.POST_commentaire()
    
      elif len(self.path_infos) >0 and self.path_infos[0]== "utilisateur":
        self.POST_utilisateur()
    
      else:
        self.send_static()
          
    # """ Gestion des commentaires
    
    #Création d'un commentaire      
    def POST_commentaire(self):
        print("Post_commentaire")
        
        #récupération de la table
        dic = ast.literal_eval(self.body)
        
        #gestion erreur dans la saisie
        if dic["pseudo"] == "" or dic["password"] == "" or dic["date"] == "" or dic["message"] == "" :
            self.send_error(422, "Il manque des informations")
        else:
            c = conn.cursor()
            
            #récupération du mot de passe pour cet utilisateur
            c.execute("SELECT pwd FROM utilisateurs WHERE pseudo = '" + dic["pseudo"] + "'")
            
            #vérification du mot de passe entrée avec le mot de passe issue de la table
            t = False
            utilisateurs = c.fetchall()
            for utilisateur in utilisateurs:
                if utilisateur[0] == dic["password"]:
                    t = True
                    
                   
            if t:
                
                #on récupère la date
                date = datetime.datetime.today().ctime()
                
                #on récupère le nombre de commentaire (ce sera son ID)
                c.execute("SELECT COUNT(*) FROM commentaires")
                count = c.fetchone()[0]
                
                #création du commentaire dans la base de donnée
                inser = "INSERT INTO commentaires VALUES ("
                inser += "'"+str(count)+"',"
                inser += "'"+dic["pseudo"]+"',"
                inser += "'"+dic["site"]+"',"
                inser += "'"+date+"',"
                inser += "'"+dic["message"]+"',"
                inser += "'"+dic["date"]+"')"
                c = c.execute(inser)
                conn.commit()
                dic["timestamp"] = date
                self.send_json(dic)
                
            #erreur si le mot de passe rentré n'est pas le bon
            else :
                self.send_error(401,"Le mot de passe ou le pseudo sont incorrects")  


  #Méthode des requêtes DELETE
    def do_DELETE(self):
        self.parametres()

        if len(self.path_infos) > 0 and self.path_infos[0] == "commentaire":
            self.delete_commentaire()
        else:
            self.send_static()

    #Récupération des commentaires
    def get_commentaire(self):
        print("Get commentaire")
    
    #récupération des commentaires
        L = []
        c = conn.cursor()
        c.execute("SELECT * FROM Commentaires WHERE site= '" + self.path_infos[1]+"'")
        data = c.fetchall()
        
        if data == []:
            self.send_error(401,"Soyez le premier à poster un commentaire")  
        
        else:
            for d in data:
                dic = {"id":d[0],
                       "pseudo": d[1],
                       "site":d[2],
                       "message":d[4],
                       "date":d[5],
                       "timestamp":d[3]}
                L.append(dic)
            self.send_json(L)
    
    #Suppression d'un commentaire
    def delete_commentaire(self):
        print("Delete_commentaire")
    #récupération de l'utilisateur
        dic = ast.literal_eval(self.body)
        c = conn.cursor()
        c.execute("SELECT * FROM utilisateurs WHERE pseudo = '" + dic["pseudo"]+"'")
        utilisateurs = c.fetchall()
    
    #vérification de l'utilisateur
        t = False
        for utilisateur in utilisateurs:
            if dic["password"] == utilisateur[2]:
                t = True
    
        if t:
          
          #suppression du commentaire
            c.execute("DELETE FROM commentaires WHERE id= '" + self.path_infos[1]+"'")
            conn.commit()
            self.send_response(204)
            self.send_json(dic)
          
     # erreur si ce n'est pas le bon passeword
        else:
          self.send_error(410, "Le mot de passe est incorrect")

    #Création d'un utilisateur
    def POST_utilisateur(self):
        print("Post_utilisateur")
          #récupération de la base de donnée
        dic = ast.literal_eval(self.body)
          
          #vérification qu'il ne manque pas d'information dans la saisie
        if dic["user_pseudo"] == "" or dic["email"] == "" or dic["user_password"] == "" :
            self.send_error(422, "Il manque des informations")
        else:
              
              #récupération du pseudo
            c = conn.cursor()
            c.execute("SELECT pseudo FROM utilisateurs")
            t = True
            utilisateurs = c.fetchall()
              
              #vérification que le pseudo n'existe pas déjà
            print(dic["user_pseudo"])
            for utilisateur in utilisateurs:
               if utilisateur[0] == dic["user_pseudo"]:
                      t = False
            print(t)
            if t:                 
                  #création de l'utilisateur
                  inser = "INSERT INTO utilisateurs VALUES ("
                  inser += "'"+dic["user_pseudo"]+"',"
                  inser += "'"+dic["email"]+"',"
                  inser += "'"+dic["user_password"]+"')"
                  c = c.execute(inser)
                  conn.commit()
                  self.send_json(dic)
                  
              #renvoie une erreur si le pseudo existe déjà
            else:
                self.send_error(409, "Le pseudo existe déjà") 
                
                
                
# """ Fonctions des TD par forcément utils par la suite """

    def send_time(self):
         self.path= self.static_dir + self.path
         # on récupère l'heure
         time = self.date_time_string()
    
         # on génère un document au format html
         body = '<!doctype html>' + \
                '<meta charset="utf-8">' + \
                '<title>l\'heure</title>' + \
                '<div>Voici l\'heure du serveur :</div>' + \
                '<pre>{}</pre>'.format(time)
    
         # pour prévenir qu'il s'agit d'une ressource au format html
         headers = [('Content-Type','text/html;charset=utf-8')]
    
         # on envoie
         self.send(body,headers)
         
    #envoyer la liste des ponts
    def send_ponts(self):
       self.path= self.static_dir + self.path
       #on récupère les données
       c.execute("SELECT name from ponts")
       
       datas=c.fetchall()
       
       #on génère doc html
       body = '<!doctype html>' + \
              '<meta charset="utf-8">' + \
              '<title>les ponts</title>' + \
              '<div>Voici les données du serveur :</div>' + \
              '<pre>{}</pre>'.format(datas)
  
       # pour prévenir qu'il s'agit d'une ressource au format html
       headers = [('Content-Type','text/html;charset=utf-8')]
  
       # on envoie
       self.send(body,headers)
    
    #envoyer les infos relatives à un ponts 
    def send_pont(self,pont):

        #on récupère les données
        c.execute("SELECT * from ponts where name = '{}'".format(pont))
        
        datas=c.fetchall()
        
        #on génère doc html
        body = '<!doctype html>' + \
               '<meta charset="utf-8">' + \
               '<title>les ponts</title>' + \
               '<div>Voici les données du pont {} :</div>'.format(pont) + \
               '<pre>{}</pre>'.format(datas)
   
        # pour prévenir qu'il s'agit d'une ressource au format html
        headers = [('Content-Type','text/html;charset=utf-8')]
   
        # on envoie
        self.send(body,headers)
        
     
    # """ Envoie de la requête """  
    
    def send(self,body,headers=[]):

      # on encode la chaine de caractères à envoyer
      encoded = bytes(body, 'UTF-8')
    
      # on envoie la ligne de statut
      self.send_response(200)
    
      # on envoie les lignes d'entête et la ligne vide
      [self.send_header(*t) for t in headers]
      self.send_header('Content-Length',int(len(encoded)))
      self.end_headers()
    
      # on envoie le corps de la réponse
      self.wfile.write(encoded)
     

        
    # """ Requête en JSON """  
        
    def send_json_ponts(self):
        self.path= self.static_dir + self.path
        #on récupère les données
        c.execute("SELECT name,lat,lon from ponts")
        
        res=c.fetchall()

        # on renvoie une liste de dictionnaires au format JSON
        data = [{"name":d[0],"lat":d[1],"lon":d[2]} for d in res]
        
        self.send_json(data)
        
        
        
        
    def send_json_pont(self,pont):
        #on récupère les données
        c.execute("SELECT * from ponts where name = '{}'".format(pont))
        res=c.fetchall()[0]
        if res == None:
            self.send_error(404,"Le Pont n'a pas été trouvé")
        # on renvoie un dictionnaire au format JSON
        else:
            data = {"dbpedia":res[0],
                   "name":res[1],
                   "wiki":res[5],
                   "desc":res[8],
                   "photo":res[9],
                   "length":res[2],
                   "span":res[3],
                   "year":res[4],
                   "lat":res[6],
                   "lon":res[7],}
        
        #on envoie la commande
        self.send_json(data)
        
    # Envoie d'un document en Json
    def send_json(self,data):
      headers = [('Content-Type','application/json')]
      self.send(json.dumps(data),headers)

""" Connexion à la base de donnée """

dbname = '{}.db'.format("ponts")
conn = sqlite3.connect(dbname)
c = conn.cursor()

conn.row_factory = sqlite3.Row
""" Lancement du serveur """

httpd = socketserver.TCPServer(("", 8080), RequestHandler)


httpd.serve_forever()
