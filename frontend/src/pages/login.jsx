import LoginForm from "../components/LoginForm";


function login() {
    return  <LoginForm route="/users/token/" method="login" />
}

export default login