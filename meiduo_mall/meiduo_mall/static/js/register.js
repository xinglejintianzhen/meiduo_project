let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data:{
        // v-model
        username: '',
        password: '',
        password2: '',
        mobile: '',
        allow: '',
        image_code: '',
        sms_code_tip: '获取短信验证码',
        send_flag: false,

    //    v-show
        error_name: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,
        error_image_code: false,
        error_sms_code: false,

    //    error_message
        error_name_message: '',
        error_mobile_message: '',
        error_image_code_message: '',
        error_sms_code_message: '请填写短信验证码',

        image_code_url: '',
        uuid: '',

    },
    mounted(){
        this.generate_image_code();
    },
    methods:{
        // 发送短信验证码
        send_sms_code(){   //  验证是否点击过
        if(this.send_flag == true){
            return;}
        this.send_flag = true;
        this.check_mobile();        // 验证手机和验证码
        this.check_image_code();
        if( this.error_image_code ==true || this.error_mobile == true){
            return;
        }
        let url = '/sms_codes/' + this.mobile + '/?image_code=' + this.image_code + '&uuid=' + this.uuid;
        axios.get(url, {
            responseType: 'json'
        })
            .then(response => {
                if(response.data.code == 0){
                    // 展示60秒倒计时结果, setInerval的两个参数，分别是回调函数和时间间隔
                    let num = 60;
                    let t = setInterval(() => {
                        if(num == 1){
                            clearInterval(t);
                            this.sms_code_tip = '获取短信验证码';
                            this.generate_image_code();
                            this.send_flag = false;
                        }else {
                        num -= 1;
                        this.sms_code_tip = num + '秒';
                        }
                    }, 1000)

                }else {
                    if(response.data.code == 4001){
                        this.error_image_code_message = response.data.errmsg;
                        this.error_image_code = true;
                    }else {  // 频繁发送的状态码4002
                        this.error_sms_code_message = response.data.errmsg;
                        this.error_sms_code = true;
                    }
                    this.send_flag = false;
                }

            })
                .catch(error => {
                    console.log(error.response);
                    this.send_flag = false;
                })
        },
        //    生成图形验证码
        generate_image_code(){
            this.uuid = generateUUID();
             this.image_code_url = '/images_codes/' + this.uuid + '/';
        },
    //    校验用户名
        check_username(){
        //    5-20个字符
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if(re.test(this.username)){
                this.error_name=false;
            }else {
                this.error_name_message = '请输入5-20个字符的用户名';
                this.error_name = true;
            }
            if(this.error_name == false){
                let url = '/usernames/' + this.username + '/count';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {if(response.data.count == 1){
                        this.error_name_message = '用户名已存在';
                        this.error_name = true;
                    }else {
                            this.error_name = false;
                    }})
                    .catch(error => {console.log(error.response)});
            }

        },
        check_password(){
            let re = /^[a-zA-Z0-9]{8,20}$/;
            if(re.test(this.password)){
                this.error_password = false;
            }else {
                this.error_password = true;
            }

        },
        check_password2(){
            if(this.password != this.password2){
                this.error_password2 = true;
            }else{
                this.error_password2 = false;
            }

        },
        check_mobile(){
        let re = /^1[3-9]\d{9}$/;
        if(re.test(this.mobile)) {
            this.error_mobile = false;
        } else {
            this.error_mobile_message = '您输入的手机号格式不正确';
            this.error_mobile = true;
        }
        if(this.error_mobile == false){
                let url = '/mobile/' + this.mobile + '/count';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {if(response.data.count == 1){
                        this.error_mobile_message = '该手机号已注册';
                        this.error_mobile = true;
                    }else {
                            this.error_mobile = false;
                    }})
                    .catch(error => {console.log(error.response)});
            }
    },
        check_image_code(){
            if(this.image_code.length != 4){
                this.error_image_code_message = '请输入正确的图形验证码';
                this.error_image_code = true;
            }else {
                this.error_image_code = false;
            }

        },
            // 校验短信验证码
        check_sms_code(){
            if(this.sms_code.length != 6){
                this.error_sms_code_message = '请填写正确的短信验证码';
                this.error_sms_code = true;
            } else {
                this.error_sms_code = false;
            }
        },

        check_allow(){
            if(!this.allow){
                this.error_allow = true;
            }else{
                this.error_allow = false;
            }
        },
        on_submit(){
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_sms_code()
            this.check_allow();

            if(this.error_name == true || this.error_password==true || this.error_password2==true || this.error_mobile==true || this.error_sms_code==true || this.error_allow==true){
                window.event.returnValue = false;
            }
        },

    },
});