## 1. Requisitos Funcionais

&emsp;&emsp; Os Requisitos Funcionais descrevem o comportamento esperado do sistema em termos de suas funcionalidades, especificando o que o sistema deve fazer para atender às necessidades dos usuários. No contexto de streaming de música, a continuidade da reprodução é um aspecto crítico, especialmente quando ocorrem falhas no servidor de streaming.

### RF-01: Continuidade da Reprodução em Caso de Falha no Servidor

&emsp;&emsp; O sistema deve garantir que a música continue tocando mesmo que ocorra uma falha no servidor de streaming, desde que o buffer tenha sido carregado adequadamente. Isso assegura uma experiência contínua para o usuário, sem interrupções perceptíveis no áudio. O buffering local (armazenamento temporário de dados) deve ser utilizado para manter a reprodução até que o servidor seja restabelecido ou reconectado.
- **Código relacionado:**
    ```gherkin
    Scenario: A música continua tocando mesmo após falha no servidor de streaming
      Given o usuário está ouvindo uma música no Spotify
      And a música foi carregada no buffer
      When ocorre uma falha no servidor responsável pelo streaming
      Then o sistema deve utilizar do buffering para continuar tocando a música
      And a qualidade do áudio não deve ser degradada durante a falha do servidor
      And o sistema deve tentar reconectar automaticamente ao servidor
      And quando a conexão for restaurada, a reprodução deve continuar sem reiniciar a música
    ```
- **Código de teste relacionado:**
    ```python
    @then('o sistema deve utilizar do buffering para continuar tocando a música')
    def step_impl(context):
        assert context.buffered is True, "O buffering não estava disponível durante a falha"
    ```

#### Caso Negativo: Falha no Buffer
- **Descrição:** Se a música não estiver armazenada no buffer e o servidor falhar, a reprodução deve ser interrompida e uma mensagem de erro deve ser exibida ao usuário.
- **Código relacionado:**
    ```gherkin
    Scenario: A música para de tocar devido à falha no servidor e falta de buffering
      Given o usuário está ouvindo uma música no Spotify
      And a música não foi carregada no buffer
      When ocorre uma falha no servidor responsável pelo streaming
      Then a reprodução da música deve ser interrompida
      And o sistema deve exibir uma mensagem de erro para o usuário
      And o sistema deve tentar reconectar automaticamente ao servidor
      And quando a conexão for restaurada, a música deve reiniciar do ponto onde parou
    ```
- **Código de teste relacionado:**
    ```python
    @then('a reprodução da música deve ser interrompida')
    def step_impl(context):
        try:
            context.is_music_playing = spotify_server.simulate_music_playback()
            assert False, "A música deveria ter parado, mas continuou tocando"
        except Exception:
            assert True
    ```

## 2. Requisitos Não Funcionais (RNF)
A seção de Requisitos Não Funcionais (RNFs) refere-se às características que não estão diretamente relacionadas com as funcionalidades do sistema, mas que são fundamentais para garantir a qualidade, desempenho e experiência do usuário. Esses requisitos buscam definir como o sistema se comporta sob diversas condições, assegurando a sua robustez, segurança e escalabilidade. Abaixo, detalho mais os RNFs mencionados, relacionando-os com normas de qualidade e categorizando-os de acordo com a ISO.

### RNF-01: Tolerância a Falhas no Servidor
&emsp;&emsp; Em caso de falha no servidor, a solução implementada deve permitir que o áudio continue sem interrupções perceptíveis ou perdas de qualidade.

**Categoria de RNF**

&emsp;&emsp; Este requisito se enquadra principalmente na categoria de Confiabilidade segundo a ISO 25010, definida pela capacidade do sistema de manter seu desempenho sob condições de falha. Além disso, está relacionada à Confiabilidade por também conseguir restaurar o serviço após uma falha.

&emsp;&emsp; Uma tática para garantir ainda mais esse requisito seria uma abordagem de streaming adaptativo ou redundância de servidores para garantir que o áudio continue sendo transmitido, mesmo diante uma queda ou problemas de conexão.

```python
@then('o sistema deve utilizar do buffering para continuar tocando a música')
def step_impl(context):
    assert context.buffered is True, "O buffering não estava disponível durante a falha"

@then('a qualidade do áudio não deve ser degradada durante a falha do servidor')
def step_impl(context):
    assert context.is_music_playing is True
```

### **RNF-02: Reconexão Automática ao Servidor**
&emsp;&emsp; Em caso de falha de conexão, o sistema deve tentar reconectar automaticamente ao servidor sem exigir qualquer ação do usuário. Além disso, ao restabelecer a conexão, a reprodução deve continuar de onde parou, sem reiniciar a música ou interromper a experiência do usuário.

**Categoria de RNF**

&emsp;&emsp; Este requisito se enquadra principalmente nas categorias de Disponibilidade e Confiabilidade, conforme a ISO 25010. A Disponibilidade refere-se à capacidade do sistema de manter o serviço funcional sem interrupções, enquanto a Confiabilidade está relacionada à capacidade do sistema de restabelecer a operação após falhas de maneira consistente e previsível.

&emsp;&emsp; A reconexão automática e a continuidade da reprodução após falha podem ser asseguradas por técnicas como tentativas de reconexão automáticas com backoff exponencial, além de garantir que o estado da música seja preservado durante a reconexão, por meio de mecanismos de cache ou armazenagem temporária dos dados necessários para a continuidade da reprodução.

```python
@then('o sistema deve tentar reconectar automaticamente ao servidor')
def step_impl(context):
    spotify_server.restore_connection()
    assert spotify_server.available is True, "O sistema falhou ao restaurar a conexão"

@then('quando a conexão for restaurada, a reprodução deve continuar sem reiniciar a música')
def step_impl(context):
    assert context.is_music_playing is True, "A música não continuou corretamente após a reconexão"
```