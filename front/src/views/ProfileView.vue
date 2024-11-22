<template>
  <div>
    <h1>마이페이지</h1>
    <div v-if="user">
      <p><strong>아이디:</strong> {{ user.username }}</p>
      <p><strong>닉네임:</strong> {{ user.nickname }}</p>
      <p><strong>이메일:</strong> {{ user.email }}</p>

      <div v-if="user.favorite_genres && user.favorite_genres.length > 0">
        <p><strong>선호 장르:</strong></p>
        <div class="genre-tags">
          <span v-for="genre in user.favorite_genres" :key="genre.id" class="genre-tag">
            {{ genre.name }}
          </span>
        </div>
      </div>
      <div v-else>
        <p>선호 장르를 선택해주세요!</p>
      </div>
    </div>
    <div v-else>
      <p>로그인 후 이용 가능합니다.</p>
    </div>

    <button @click="openGenreModal">선호 장르 선택</button>
    <button @click="editProfile">회원 정보 수정</button>
    <button @click="deleteAccount">회원 탈퇴</button>
    <button @click="logout">로그아웃</button>

    <GenreSelectModal
      v-if="isGenreModalOpen"
      :selectedGenres="selectedGenres"
      @update:selectedGenres="updateSelectedGenres"
      @save="saveSelectedGenres"
      @close="closeGenreModal"
    />
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/authStore";
import GenreSelectModal from "@/components/GenreSelectModal.vue";
import axios from "axios";

export default {
  name: "ProfileView",
  components: { GenreSelectModal },
  data() {
    return {
      user: null,
      isGenreModalOpen: false,
      selectedGenres: [],
    };
  },
  async created() {
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated) {
      alert("로그인이 필요합니다!");
      this.$router.push("/login");
      return;
    }

    try {
      this.user = await authStore.fetchUserProfile();
      this.selectedGenres = this.user.favorite_genres?.map((genre) => genre.id) || [];
    } catch (error) {
      console.error("프로필 정보를 가져오는 중 오류 발생:", error);
      alert("사용자 정보를 불러오지 못했습니다. 다시 로그인 해주세요.");
      authStore.logout();
      this.$router.push("/login");
    }
  },
  methods: {
    openGenreModal() {
      this.isGenreModalOpen = true;
    },
    closeGenreModal() {
      this.isGenreModalOpen = false;
    },
    updateSelectedGenres(newGenres) {
      this.selectedGenres = newGenres;
    },
    async saveSelectedGenres() {
      try {
        const authStore = useAuthStore();
    
        console.log("Selected genres to save:", this.selectedGenres); // 디버그 로그

        const updatedUser = await authStore.updateFavoriteGenres(this.selectedGenres);

    // 즉시 `user.favorite_genres`를 업데이트하여 UI 반영
        this.user.favorite_genres = updatedUser.favorite_genres.map((genre) => ({
          id: genre.id,
          name: genre.name,
        }));

        alert("선호 장르가 업데이트되었습니다.");
        this.closeGenreModal();
      } catch (error) {
        console.error("선호 장르 업데이트 중 오류 발생:", error.response?.data || error);
        alert("선호 장르 업데이트에 실패했습니다. 다시 시도해주세요.");
      }
    },

    editProfile() {
      this.$router.push("/profile/edit");
    },
    async deleteAccount() {
      try {
        await axios.delete("/accounts/profile/", {
          headers: {
            Authorization: `Token ${localStorage.getItem("authToken")}`,
          },
        });
        alert("회원 탈퇴가 완료되었습니다.");
        const authStore = useAuthStore();
        authStore.logout();
        this.$router.push("/");
      } catch (error) {
        console.error("회원 탈퇴 중 오류 발생:", error);
        alert("회원 탈퇴에 실패했습니다. 다시 시도해주세요.");
      }
    },
    logout() {
      const authStore = useAuthStore();
      authStore.logout();
      alert("로그아웃 되었습니다.");
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.genre-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.genre-tag {
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 5px 10px;
}
</style>
