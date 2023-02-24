import './HeaderNavbar.less';

export default function HeaderNavbar() {
  return (
    <div className='header-navigation'>
      <div className='o-header_logo'>
        <a href='/'>
          <img
            className='o-header_logo-img'
            src='/static/images/logo_237x50@2x.png'
            alt='Consumer Financial Protection Bureau'
            width='237'
            height='50'
          />
        </a>
      </div>
    </div>
  );
}
