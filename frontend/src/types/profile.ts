export interface ProfileData {
  display_name: string;
  avatar_url: string;
  age: number | null;
  challenge_preferences: Record<string, boolean>;
}