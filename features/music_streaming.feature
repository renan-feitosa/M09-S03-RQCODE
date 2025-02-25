Feature: Confiabilidade do Streaming de Música no Spotify

    Scenario: A música continua tocando mesmo após falha no servidor de streaming
        Given o usuário está ouvindo uma música no Spotify
        And a música foi carregada no buffer
        When ocorre uma falha no servidor responsável pelo streaming
        Then o sistema deve utilizar do buffering para continuar tocando a música
        And a qualidade do áudio não deve ser degradada durante a falha do servidor
        And o sistema deve tentar reconectar automaticamente ao servidor
        And quando a conexão for restaurada, a reprodução deve continuar sem reiniciar a música
    
    Scenario: A música para de tocar devido à falha no servidor e falta de buffering
        Given o usuário está ouvindo uma música no Spotify
        And a música não foi carregada no buffer
        When ocorre uma falha no servidor responsável pelo streaming
        Then a reprodução da música deve ser interrompida
        And o sistema deve exibir uma mensagem de erro para o usuário
        And o sistema deve tentar reconectar automaticamente ao servidor
        And quando a conexão for restaurada, deve reiniciar a reprodução
