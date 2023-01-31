import './App.less';
import HeaderNavbar from './components/HeaderNavbar';

export default function App() {
  return (
    <main id='main' role='main'>
      <header>
        <HeaderNavbar />
      </header>
      <div className='App block block__sub'>
        <h1>Metro2 Evaluator Tool</h1>
      </div>
    </main>
  );
}
