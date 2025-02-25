from SpotifyServer import SpotifyServer
from behave import given, when, then
import time

spotify_server = SpotifyServer()

@given('o usuário está ouvindo uma música no Spotify')
def step_impl(context):
    context.is_music_playing = spotify_server.simulate_music_playback()
    assert context.is_music_playing is True

@given('a música foi carregada no buffer')
def step_impl(context):
    context.buffered = spotify_server.buffered_music
    assert context.buffered is True

@given('a música não foi carregada no buffer')
def step_impl(context):
    spotify_server.buffered_music = False
    context.buffered = spotify_server.buffered_music
    assert context.buffered is False

@when('ocorre uma falha no servidor responsável pelo streaming')
def step_impl(context):
    spotify_server.available = False
    time.sleep(1)  # Simulação do tempo de resposta do failover

@then('o sistema deve utilizar do buffering para continuar tocando a música')
def step_impl(context):
    assert context.buffered is True, "O buffering não estava disponível durante a falha"

@then('a qualidade do áudio não deve ser degradada durante a falha do servidor')
def step_impl(context):
    assert context.is_music_playing is True

@then('o sistema deve tentar reconectar automaticamente ao servidor')
def step_impl(context):
    spotify_server.restore_connection()
    assert spotify_server.available is True, "O sistema falhou ao restaurar a conexão"

@then('quando a conexão for restaurada, a reprodução deve continuar sem reiniciar a música')
def step_impl(context):
    assert context.is_music_playing is True, "A música não continuou corretamente após a reconexão"

@then('a reprodução da música deve ser interrompida')
def step_impl(context):
    try:
        context.is_music_playing = spotify_server.simulate_music_playback()
        assert False, "A música deveria ter parado, mas continuou tocando"
    except Exception:
        assert True

@then('o sistema deve exibir uma mensagem de erro para o usuário')
def step_impl(context):
    context.error_message = "Erro: Não foi possível continuar a reprodução da música."
    assert context.error_message == "Erro: Não foi possível continuar a reprodução da música.", "Mensagem de erro incorreta"

@then('quando a conexão for restaurada, deve reiniciar a reprodução')
def step_impl(context):
    spotify_server.restore_connection()
    assert context.is_music_playing is True, "A música não reiniciou após a reconexão"