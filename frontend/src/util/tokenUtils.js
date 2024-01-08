import { jwtDecode } from 'jwt-decode';
import store from '@/store';


export async function isTokenValid(token) {
  if (!token) {
    return false;
  }

  try {
    const decodedToken = jwtDecode(token);
    const currentTime = Date.now() / 1000;

    if (decodedToken.exp && decodedToken.exp < currentTime) {
      // If the token is not valid, attempt to refresh it
      const refreshSuccess = await store.dispatch('refreshToken');

      if (!refreshSuccess) {
        // If refreshing fails, execute userLogout
        await store.dispatch('userLogout');
        return false;
      }

      // If refreshing succeeds, return true
      return true;
    }

    return true;
  } catch (error) {
    // If there's an error decoding the token, execute userLogout
    await store.dispatch('userLogout');
    return false;
  }
}
