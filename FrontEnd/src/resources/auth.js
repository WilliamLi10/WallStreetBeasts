// utils/auth.js
export const isLoggedIn = () => {
    const token = document.cookie
      .split('; ')
      .find(row => row.startsWith('token='));
    return Boolean(token);
  };
  