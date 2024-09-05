from flask import Blueprint, session, request
import os
import importlib
import inspect

main_routes = Blueprint('main_routes', __name__)

class Routes:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.register_routes()


    def register_routes(self):

        # Registra a rota dinâmica sem parâmetros adicionais
        self.blueprint.add_url_rule('/<route_name>', 'route_name', self.route_name, methods=["GET", "POST"])

        # Registra a rota dinâmica com  method adicionais
        self.blueprint.add_url_rule('/<route_name>/<method>', 'route_method', self.route_method, methods=["GET", "POST"])

        # Registra a rota dinâmica com parâmetros adicionais
        self.blueprint.add_url_rule('/<route_name>/<method>/<parameter>', 'route_param', self.route_param, methods=["GET", "POST"])


    def route_name(self, route_name):
        # O parâmetro route_name é passado diretamente pela URL
        return self.handle_logic(route_name)

    def route_method(self, route_name, method=None):
        # Os parâmetros route_name e paramenter são passados diretamente pela URL
        return self.handle_logic(route_name, method)
    
    def route_param(self, route_name, method=None, parameter=None):
    # Os parâmetros route_name e paramenter são passados diretamente pela URL
        return self.handle_logic(route_name, method, parameter)


    def handle_logic(self, route_name, method=None, parameter=None):
        route_name = self.standardizeController(route_name)

        if method is not None:
            method = self.standardizeMethod(method)

        # Carrega arquivo que foi chamado pelo valores da url, onde baser_dir é o dir atual de routes
        base_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_arquivo = os.path.join(base_dir, "controller", route_name + ".py")

        if os.path.exists(caminho_arquivo):

            modulo = importlib.import_module("finalProject.controller." + route_name)

            # sso geralmente significa que você está tentando acessar ou modificar a session fora do contexto de uma requisição HTTP 
            session["request_method"] = request.method

            print(session["request_method"])
            # print(method)
            if method is None and hasattr(modulo, route_name):
                classe = getattr(modulo, route_name)

                if hasattr(classe, self.standardizeMethod(route_name)):
                    funcao = getattr(classe,  self.standardizeMethod(route_name))

                    return funcao()

            elif method is not None and hasattr(modulo, route_name):
                classe = getattr(modulo, route_name)

                classe_instance = classe()
                
                if hasattr(classe_instance, method):
                    funcao = getattr(classe_instance, method)
                        
                    return self.verifyParamenter(funcao, parameter)
                
                return "method n existe", 404
            else:
                return "route_name n existe", 404
        else:
            return "arquivo n existe", 404


    @main_routes.errorhandler(404)
    def page_not_found(e):
        # Exibe uma página customizada ou mensagem para o usuário
        return "A URL solicitada não foi encontrada no servidor. Por favor, verifique a URL e tente novamente.", 404


    @main_routes.errorhandler(500)
    def page_not_found(e):
        # Exibe uma página customizada ou mensagem para o usuário
        return "Consulte os proprietarios do site", 500


    def verifyParamenter(self, funcao, parameter):
        """
        funcao: receba a função da classe
        parameter: recebe o parameter pela url

        A função verifyParamenter verifica se esta função recebe um parameter, caso receba, verifica se é obrigatorio ou opcional, 
        e tambem verifica se o parameter é nulo ou possui um valor, caso n receba apenas retorna a função
        """

        signature = inspect.signature(funcao)
        params = signature.parameters
        
        if(len(signature.parameters) != 0) :
            for param_name, param in params.items():
                if param_name == "self":
                    continue  # Ignore o parâmetro 'self'

                #param.default: Refere-se ao valor padrão do parâmetro, dentro da assinatura da função. Se o parâmetro não tiver um valor padrão, param.default será inspect.Parameter.empty.
                #Veficar se o paramentro da classe é obrigatio e se o paramentr é vazio
                if param.default == inspect.Parameter.empty and parameter is None:
                    print(f'O parâmetro "{param_name}" é obrigatório.')
                    return "parametro obrigartio", 404
                #Veficar se o paramentro da classe é opcional e se o paramentr é vazio
                elif(parameter is not None or param.default != inspect.Parameter.empty):
                    print(f'O parâmetro "{param_name}" é opcional.')
                    # return funcao(parameter)                 
                    return funcao(parameter) 

            return funcao()
        else:
            return funcao()


    def standardizeController(self, route):
        route = route.lower()

        route = route.replace(" ", "")

        route = route.replace("-", "_")

        route = route.capitalize()

        print(route)
        return route


    def standardizeMethod(self, method):
        # method = method.lower().replace("-", " ").title().replace(" ", "")
        method = method.lower()

        method = method.replace("-", " ")

        method = method.title()

        method = method.replace(" ", "")

        method = method[0].lower() + method[1:]

        return method


routes = Routes(main_routes)
