export default function Home() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center bg-zinc-50 px-6 py-16 dark:bg-black">
      <main className="flex w-full max-w-xl flex-col items-center gap-6 text-center">
        <h1 className="text-5xl font-semibold tracking-tight text-black dark:text-zinc-50">
          Pics
        </h1>
        <p className="text-lg leading-8 text-zinc-600 dark:text-zinc-400">
          Sua galeria de fotos. Em breve você poderá enviar e organizar suas
          imagens por aqui.
        </p>
        <a
          href="http://localhost:8000/docs"
          className="rounded-full bg-black px-6 py-3 text-base font-medium text-white transition-colors hover:bg-zinc-800 dark:bg-white dark:text-black dark:hover:bg-zinc-200"
        >
          Documentação da API
        </a>
      </main>
    </div>
  );
}
