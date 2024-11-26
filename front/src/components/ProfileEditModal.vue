<template>
<div class="modal-container">
  <div class="modal-content">
  <h2>회원 정보 수정</h2>
  <form @submit.prevent="submitForm">
    <div class="form-group">
      <label for="nickname">닉네임</label>
      <input
        v-model="updatedUser.nickname"
        id="nickname"
        type="text"
        placeholder="닉네임을 입력하세요"
        required
      />
    </div>
    <div class="form-group">
      <label for="email">이메일</label>
      <input
        v-model="updatedUser.email"
        id="email"
        type="email"
        placeholder="이메일을 입력하세요"
        required
      />
    </div>
    <div class="modal-actions">
      <button type="submit">저장</button>
      <button type="button" @click="$emit('close')">취소</button>
    </div>
  </form>
  </div>
</div>
</template>
  
<script>
import { useAuthStore } from "@/stores/authStore";

export default {
  name: "ProfileEditModal",
  props: {
    user: {
      type: Object,
      required: true,
      default: () => ({
        id: null,
        username: "",
        nickname: "",
        email: "",
      }),
    },
  },
  data() {
    return {
      updatedUser: { ...this.user }, // 초기값 복사
    };
  },
  methods: {
    async submitForm() {
      const authStore = useAuthStore();
      try {
        const updatedProfile = await authStore.updateUserProfile(this.updatedUser);
        this.$emit("update:user", updatedProfile); // 부모 컴포넌트로 업데이트 알림
        alert("회원 정보가 수정되었습니다.");
        this.$emit("close");
      } catch (error) {
        console.error("회원 정보 수정 중 오류 발생:", error);
        alert("회원 정보 수정에 실패했습니다.");
      }
    },
  },
};
</script>

<style scoped>
.modal-container {
position: fixed;
top: 0;
left: 0;
width: 100%;
height: 100%;
background: rgba(0, 0, 0, 0.5);
display: flex;
justify-content: center;
align-items: center;
z-index: 1000;
}

.modal-content {
background: white;
padding: 20px;
border-radius: 10px;
width: 400px;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
text-align: center;
}

.modal-actions {
display: flex;
justify-content: space-between;
margin-top: 20px;
}

.modal-actions button {
padding: 10px 20px;
border: none;
border-radius: 5px;
cursor: pointer;
}

.modal-actions button:first-child {
background-color: #007bff;
color: white;
}

.modal-actions button:last-child {
background-color: #dc3545;
color: white;
}
</style>