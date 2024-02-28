class CandidateImage {
    url: string
    caption?: string

    constructor(url: string, caption?: string) {
        this.url = url;
        this.caption = caption;
    }
}

export { CandidateImage }