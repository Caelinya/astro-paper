export const SITE = {
  website: "https://caelinya.im/", // replace this with your deployed domain
  author: "Caelinya",
  profile: "https://caelinya.im/",
  desc: "A personal blog by Caelinya about cybersecurity, web development, and technology.",
  title: "Caelinya",
  ogImage: "astropaper-og.jpg",
  lightAndDarkMode: true,
  postPerIndex: 4,
  postPerPage: 4,
  scheduledPostMargin: 15 * 60 * 1000, // 15 minutes
  showArchives: true,
  showBackButton: true, // show back button in post detail
  editPost: {
    enabled: true,
    text: "Suggest Changes",
    url: "https://github.com/caelinya/astro-paper/edit/main/",
  },
  dynamicOgImage: true,
  lang: "en", // html lang code. Set this empty and default will be "en"
  timezone: "America/Los_Angeles", // Default global timezone (IANA format) https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
} as const;

export const SHIKI_CONFIG = {
  themes: {
    light: "material-theme-lighter",
    dark: "github-dark",
  },
  wrap: true,
};
