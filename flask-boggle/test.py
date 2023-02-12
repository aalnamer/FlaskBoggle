from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    
    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/board")
            self.assertIn('board',session)
            self.assertIn(b'<p>High Score:', resp.data)
            self.assertIn(b'Score:', resp.data)
            self.assertIn(b'Seconds Left:', resp.data)
            self.assertIsNone(session.get('nplays'))
            self.assertEqual(resp.status_code, 200)
            
    def test_valid(self):
        with app.test_client() as client:
            with client.session_transaction as current_session:
                current_session['board'] = [["B","A","L","L","L"],
                                            ["B","A","L","L","L"],
                                            ["B","A","L","L","L"],
                                            ["B","A","L","L","L"],
                                            ["B","A","L","L","L"],]
                resp = self.client.get('/check-word?word=ball')
                self.assertEqual(resp.json['result'], 'ok')
    def test_invalid(self):
        self.client.get("/board")
        resp = self.client.get('/check-word?word=ompossible')
        self.assertEqual(resp.json['result'], 'not-on-board')
        
    def test_not_exist(self):
        self.client.get("/board")
        resp = self.client.get('/check-word?word=lakwesdsf')
        self.assertEqual(resp.json['result'], 'not-word')
